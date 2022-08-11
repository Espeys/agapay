import logging
from django import forms
from django.conf import settings as django_settings
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db.models import Q
from . import fields, serializers


logger = logging.getLogger(__name__)


class BaseStaticForm(forms.Form):
    """
    Class for all static form, expected to be paginated.
    If not a queryset or list or tuple just used the set serializer
    structure:
        if slug - q - filter, if all is provided slug will be considered first.
    """

    default_error_messages = {
        'invalid_filter': 2,
        'invalid_filter_type': 3,
        'invalid_page': 4,
        'invalid_slug_query': '5',
        'invalid_search': '6',
        'invalid_order_values': 7,
        'invalid_order_values_type': 8,
        'invalid_query': '9'
    }

    slug = forms.CharField(required=False)
    q = forms.CharField(required=False)
    filter = fields.TypedJSONField(
        required=False,
        type=dict,
        error_messages={
            'invalid': default_error_messages['invalid_filter'],
            'invalid_type': default_error_messages['invalid_filter_type']
        }
    )
    page = forms.IntegerField(
        required=False,
        error_messages={
            'invalid': default_error_messages['invalid_page']
        }
    )

    # list of string : order the queryset.
    # if not answered or all value not in order_fields
    # uses the the default query, yet if there is clean it and use it to order.
    # in django-admin this order_fields is automatic with list_display.
    # yet since this is rest-api order_fields is created.
    order_values = forms.CharField(required=False)

    serializer_class = None
    page_counter = None
    search_fields = []

    list_filter = []

    order_list = []

    # validation to check if list
    LIST_MODE_VALUE = -1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # key to override the messages again, raise key error if there is None.
        self.fields['filter'].error_messages['invalid'] = self.default_error_messages['invalid_filter']
        self.fields['filter'].error_messages['invalid_type'] = self.default_error_messages['invalid_filter_type']
        self.fields['page'].error_messages['invalid'] = self.default_error_messages['invalid_page']
        self.fields['order_values'].error_messages['invalid'] = self.default_error_messages['invalid_order_values']
        self.fields['order_values'].error_messages['invalid_type'] = self.default_error_messages['invalid_order_values_type']

    def clean_order_values(self):
        order_values = self.cleaned_data['order_values']

        if order_values:
            return order_values.split('.')

        return order_values

    def _order_list_to_dict(self, order_list, *args, **kwargs):
        """To replicate django order there was numeric were in it was base on
        list display. In this process it only needs the fields and it will
        convert the fields to positive and negative counterparts.
        """

        # start at 1 since there is no -0
        order_dict = {}

        if order_list:
            for i, o in enumerate(order_list, start=1):
                order_dict[str(i)] = o
                order_dict[str(-i)] = '-'+ o

        return order_dict

    def get_search_fields(self, *args, **kwargs):
        """
        Use in q
        """
        if not isinstance(self.search_fields, (list, tuple)):
            raise TypeError('search_fields must be a list or tuple')

        return self.search_fields

    def get_list_filter(self, *args, **kwargs):
        """
        Use in filter
        """
        if not isinstance(self.list_filter, (list, tuple)):
            raise TypeError('list_filter must be a list or tuple')

        return self.list_filter

    def get_order_list(self, *args, **kwargs):
        """
        Use in order
        """
        if not isinstance(self.order_list, (list ,tuple)):
            raise TypeError('sort_by must be a list or tuple')

        return self.order_list

    def get_final(self, out={}):
        return out

    def get_serializer_class(self, *args, **kwargs):

        if not self.serializer_class:
            raise ValueError('serializer_class must not be empty')

        return self.serializer_class

    def get_page_counter(self, *args, **kwargs):
        if self.page_counter != -1:
            return self.page_counter or django_settings.NUMBER_OF_PAGINATION
        return self.page_counter

    def get_queryset(self, *args, **kwargs):
        raise NotImplementedError('Queryset must be implemented first')

    def custom_query(self, qs, *args, **kwargs):
        """
        Override this whenever there is a custom query before passing it to
        serializer and after q or filter is executed.

        use of this for example fields do not had is_expired but rather it
        is a method def is_expired. and will be in filter class.

        must alway return a qs.

        we can safely assume it will be going in data['filter']
        and so.
        filter = data['filter']
        is_expired = filter.get('is_expired', None)

        if is_expired == True:# do the query e.g qs.filter(expired_at__lte=timezone.now())
        if is_expired == False  # do this
        return qs.
        """
        return qs

    def custom_filter(self, key=None, value=None):
        return None

    def custom_order(self, value=None):
        return None

    def custom_count(self, qs):
        return qs.count()

    def process_query(self, key, item):
        """
        Validate key if contains not string keywords e.g gte, lte, isnull
        didnt try in range but base on example range takes 2 keywords...
        else do __icontains as default.
        it should be expr = ''
        """

        # will add more
        if key.endswith(
            (
                '__gte',
                '__lte',
                '__isnull',
                '__iexact',
                '__exact',
                '__lt',
            )):
            return {key:item}

        # use the default
        # in order to use the exact use __exact
        return {'{}__icontains'.format(key): item}

    def process_order_values(self, *args, **kwargs):
        order_list = self.get_order_list(*args, **kwargs)
        order_dict = self._order_list_to_dict(order_list, *args, **kwargs)

        order_values = self.cleaned_data.get('order_values')
        orders = []

        for o in order_values:
            con_o = order_dict.get(o, None)
            if not con_o: continue
            orders.append(con_o)

        return orders

    def process_filter(self, *args, **kwargs):
        filters = Q()
        search_fields = self.get_search_fields(*args, **kwargs)
        list_filter = self.get_list_filter(*args, **kwargs)
        data_filter = self.cleaned_data['filter']

        for k, v in data_filter.items():
            filter_one = Q()

            if k in list_filter:
                v = v if type(v) in [list, tuple] else [v]
                if k.endswith(('__range', '__in')):
                    filter_one |= Q(**{k: v})
                else:
                    for i in v:
                        filter_one |= Q(**self.process_query(k, i))
            else:
                s = self.custom_filter(k, v)
                if s:
                    s = [s] if type(s) not in [list, tuple] else s
                    for _s in s:
                        # assuming all values were cleaned in custom_filter
                        if isinstance(_s, (Q,)): filter_one &= _s
                        else:filter_one &= Q(**_s)
                else:
                    return Q(None)

            filters &= filter_one

        return filters

    def process_q(self, *args, **kwargs):
        search_fields = self.get_search_fields(*args, **kwargs)
        data_q = self.cleaned_data['q']
        filters = Q()

        for i in search_fields:
            filters |= Q(**self.process_query(i, data_q))

        return filters

    def _final_out(self, serialize_out, *args, **kwargs):
        return serializers.PaginatedObject(serialize_out).data

    def handle(self, *args, **kwargs):
        # based pagination handler
        data = self.cleaned_data
        qs = self.get_queryset(*args, **kwargs)
        serializer_class = self.get_serializer_class(*args, **kwargs)
        page_counter = self.get_page_counter(*args, **kwargs)
        query_q = None
        query_filter = None

        # get
        if data['slug']:
            try:
                qs = qs.get(slug=data['slug'])
            except:
                raise ValidationError(self.default_error_messages['invalid_slug_query'])
            return serializer_class(qs).data

        # list with filters and q
        if data['q']:
            query_q = self.process_q(*args, **kwargs)

        if data['filter']:
            query_filter = self.process_filter(*args, **kwargs)

        try:
            if query_q:
                qs = qs.filter(query_q)
            if query_filter:
                qs = qs.filter(query_filter)
        except Exception as e:
            qs = qs.none()
            #logger.exception(e)
            #raise ValidationError(self.default_error_messages['invalid_query'])

        # if order_values
        if data['order_values']:
            qs = qs.order_by(*self.process_order_values(*args, **kwargs))

        # build paginator
        out = {}
        count = self.custom_count(qs)
        base_count = 1

        if page_counter == self.LIST_MODE_VALUE:
            out['count_per_page'] = count
            out['start_page'] = base_count
            out['page'] = base_count
            out['last_page'] = base_count
            out['total_pages'] = base_count
            out['start_index'] = base_count
            out['last_index'] = base_count
            out['total_count'] = count
            out['total_results'] = count
            out['items'] = serializer_class(qs, many=True).data
        else:
            paginated_query = Paginator(
                qs,
                page_counter
            )

            page = min(
                max(1, self.cleaned_data['page'] or 1),
                paginated_query.num_pages
            )

            paginated_page = paginated_query.get_page(page)
            page_range = paginated_query.page_range

            out['count_per_page'] = page_counter
            out['start_page'] = page_range.start
            out['page'] = paginated_page.number
            out['last_page'] = page_range.stop - 1
            out['total_pages'] = paginated_query.num_pages

            # duplicate
            out['start_index'] = paginated_page.start_index()
            out['last_index'] = paginated_page.end_index()
            out['total_count'] = paginated_query.count
            out['total_results'] = count

            out['items'] = serializer_class(paginated_page, many=True).data

        # final output, refactor this
        out = self.get_final(out)
        out = self._final_out(out, *args, **kwargs)
        return out
