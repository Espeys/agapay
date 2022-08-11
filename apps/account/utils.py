from django.contrib.auth import (
    authenticate,
    login,
    get_user_model,
)


User = get_user_model()


def check_user_exists(email, *args, **kwargs):
    try:
        User.objects.get(username=email)
    except User.DoesNotExist:
        return False
    return True


