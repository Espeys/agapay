import logging


logger = logging.getLogger(__name__)


ERRORS_DICT = {
    0: 'Please contact the system administrator. {error}',
    1: ('error', 'Error is manually triggered'),
    2: ('filter', 'Value must be a valid JSON.'),
    3: ('filter', 'Passed object was not a dictionary.'),
    4: ('page', 'Invalid format.'),
    5: ('slug', 'Query does not exists.'),
    6: ('filter', 'Query does not belong in available fields.'),
    7: ('order_values', 'Value must be a valid JSON.'),
    8: ('order_values', 'Passed object was not a list of string.'),
    9: 'Invalid query',
    10: ('slug', 'Task is required.'),
    11: ('action', 'Action is required.'),
    12: ('action', 'Chosen action was not available.'),
    13: '{error}',
}


def get_tuple_value(collection, key):
    """Returns deconstructed tuple from collection"""

    v = collection[key]

    if type(v) in [list, tuple] and len(v) == 2:
        return v
    else:
        return (None, str(v))


def parse_error(cls, exc, collection=None, key=None):
    """Automatically creates the Error response with {code, message}"""

    # Assuming Validation error
    message = getattr(exc, 'message', None) or ''
    code = getattr(exc, 'code', None)
    params = getattr(exc, 'params', None) or {}

    err = (code
           or message.format(**params)
           or str(exc).strip())

    # Use default collection if None
    collection = collection or ERRORS_DICT

    if isinstance(collection, dict):
        reverse = {}

        for k, v in collection.items():
            field, message = get_tuple_value(collection, k)
            reverse[message.strip()] = (field, k)
    else:
        reverse = {}

    if str(err).isdigit() and int(err) in collection:
        field, message = get_tuple_value(collection, int(err))

        return {
            'code': int(err),
            'message': message.format(**params),
            'field': field,
        }
    elif err in reverse:
        field, code = get_tuple_value(reverse, err)

        return {
            'code': code,
            'message': err,
            'field': field,
        }

    elif key:
        key = key if key != '__all__' else None

        return {
            'code': 13,
            'message':ERRORS_DICT[13].format(error=err),
            'field': key,
        }

    else:
        return {
            'code': 0,
            'message': ERRORS_DICT[0].format(error=err),
            'field': None,
        }
