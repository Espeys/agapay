import logging
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_tracking.mixins import LoggingMixin
from .errors import parse_error
from .serializers import GenericSerializer


logger = logging.getLogger(__name__)


class GenericView(LoggingMixin, APIView):
    errors_dict = None
    form_class = None

    def get_errors_dict(self):
        return self.errors_dict

    def get_form_class(self, request, *args, **kwargs):
        if not self.form_class:
            raise ValueError('form_class should not be empty')

        return self.form_class

    def get_params(self, request, accepts_get, *args, **kwargs):
        params = (request.data
                    or (request.query_params if accepts_get
                        else None))
        return params

    def get_request_object(self, request, *args, **kwargs):
        # in future this can be used to instant request an object
        # should validate if requested object in its method
        # currently does not support models so should be expilicit call.
        # use this before process_base_form if you want
        return None

    def process_base_form(self, base_form, params, request, *args, **kwargs):
        # override this if you want custom methods of base_form
        # but always return it.
        # through this we can do 404 in instant.
        return base_form(params, request.FILES) # should deprecated this request.FIlES

    def process(self, request, *args, **kwargs):
        """
        Automatically processes data from endpoint
        @param request - (HttpRequest)
        @out (dict) - {success, errors, data}
        """

        base_form = self.get_form_class(request, *args, **kwargs)
        accepts_get = kwargs.get('accepts_get', True)
        params = self.get_params(request, accepts_get, *args, **kwargs)

        form = self.process_base_form(base_form, params, request, *args, **kwargs)

        errors = []
        data = None

        if form.is_valid():
            try:
                data = form.handle(self, request, *args, **kwargs)
            except Exception as e:
                logger.exception(e)
                error_list = e.error_list if hasattr(e, 'error_list') else [e]

                for i in error_list:
                    errors.append(parse_error(form, i, self.get_errors_dict()))
        else:
            # this is the standard cleaned_data clean errors
            # we should clean here. Assuming all were ValidationError
            for key, val in dict(form.errors).items():
                errors.extend([parse_error(form, e, self.get_errors_dict(), key) for e in val])

        out = {
            'success': not len(errors),
            'errors': errors,
            'data': data,
        }

        return Response(GenericSerializer(out).data)
