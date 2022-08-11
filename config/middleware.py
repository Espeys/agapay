# https://github.com/DJWOMS/WomsWebSocketChat/blob/master/chat_room/chatmiddleware.py
# https://channels.readthedocs.io/en/latest/topics/authentication.html


from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware

from django.contrib.auth import AnonymousUser
from django.conf import settings as django_settings

from oauth2_provider.models import AccessToken


@database_sync_to_async
def get_user(token):
    try:
        return AccessToken.objects.get(
            token=token,
            app=django_settings.DEFAULT_APPLICATION_MODEL_NAME
        )
    except User.DoesNotExist:
        return AnonymousUser()


class OAuth2TokenWSMiddleware(BaseMiddleware):
    """Uses OAuth2 Access Token"""

    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        headers = dict(scope['headers'])

        scope['user'] = await get_user(scope["query_string"])
        return await self.inner(scope, receive, send)

def OAuth2TokenWSMiddlewareStack(inner):
    return OAuth2TokenWSMiddleware(AuthMiddlewareStack(inner))
