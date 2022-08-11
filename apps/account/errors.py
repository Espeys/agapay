import logging


logger = logging.getLogger(__name__)

CHAR_SHORT_MAX_LENGTH_DESCRIPTION = 'Exceeded maximum length of 50 characters.'
CHAR_LONG_MAX_LENGTH_DESCRIPTION = 'Exceeded maximum length of 255 characters.'


ERRORS_DICT = {
    10000: ('username', 'Username is required.'),
    10001: ('password', 'Password is required.'),
    10002: ('username', 'Invalid username or password.'),
    10003: ('username', 'User was invalid.'),


    10004: ('refresh_token', 'Refresh token is required.'),
    10005: ('refresh_token', 'Refresh token in invalid.'),
    10006: ('refresh_token', 'Refresh token already expired.'),

    10007: 'Access token is invalid.',

    10008: ('username', 'Username already exists'),
    10009: 'Password and confirm password do not match.',
    10010: '{error}',

    10011: 'User does not exists.',

    10012: 'User does not exists.',
    10013: 'You do not have permission to edit this.',

    10014: 'User does not exists.',
    10015: 'You do not have permission to edit this.',

    10016: 'User does not exists.',
    10017: 'You do not have permission to edit this.',

    10018: ('new_password', '{error}'),
    10019: ('old_password', 'Incorrect password.'),
    10020: 'Password and new password do not match.',

    10021: '{error}',
    10022: 'Password and confirm password do not match.',
    10023: 'Invalid token.',

    10024: 'User cannot follow or unfollow themselves.',


    10025: 'Invalid filter.',
    10026: 'Invalid filter type.',
    10027: 'Invalid page.',
    10028: 'Invalid slug.',
    10029: 'Invalid search.',
    10030: 'Invalid order.',
    10031: 'Invalid order values.',
    10032: 'Invalid query.',
    10033: 'Post not found.',


    10034: 'Invalid token',

    10035: 'User cannot connect themselves.',
    10036: 'User cannot report themselves.',

    10037: 'Already had a request or added.',

    10038: 'Chatroom not found.',
    10039: 'Error occured in users.',

    10040: 'Cannot add self',
    10041: 'No proper operation',
    10042: 'Already Added',
}