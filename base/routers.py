from django.utils.module_loading import import_string


class GenericRouter(object):

    def _get_model(self, app_label, model_name):
        try:
            models = import_string('{}.models'.format(app_label))
            attrs = {i.lower(): i
                     for i in dir(models)
                     if not i.startswith('_')}

            return getattr(models, attrs.get(model_name), None)
        except Exception as e:
            return None

    def _get_binding(self, obj):
        return getattr(obj, '__bind_key__', 'default')

    def db_for_read(self, model, **hints):
        return self._get_binding(model)

    def db_for_write(self, model, **hints):
        return self._get_binding(model)

    def allow_relation(self, obj1, obj2, **hints):
        return self._get_binding(obj1) == self._get_binding(obj2)

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        binding = self._get_binding(self._get_model(app_label, model_name))
        return binding == 'default'
