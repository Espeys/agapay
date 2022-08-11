import logging


logger = logging.getLogger(__name__)

CHAR_SHORT_MAX_LENGTH_DESCRIPTION = 'Exceeded maximum length of 50 characters.'
CHAR_LONG_MAX_LENGTH_DESCRIPTION = 'Exceeded maximum length of 255 characters.'


ERRORS_DICT = {
    20000: 'Invalid filter.',
    20001: 'Invalid filter type.',
    20002: 'Invalid page.',
    20003: 'Invalid slug.',
    20004: 'Invalid search.',
    20005: 'Invalid order.',
    20006: 'Invalid order values.',
    20007: 'Invalid query.',
    20008: 'Post not found.',
    20009: 'Already shared.',
    20010: 'Mood not processed.',
    20011: ('mood_type', 'Already log in a diary'),
    20012: 'Root not found',
    20013: 'Cannot comment under.',
    20014: 'Comment not found',
    20015: 'Something wrong.',
    20016: 'Support not found',
}