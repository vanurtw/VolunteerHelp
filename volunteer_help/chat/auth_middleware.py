from urllib.parse import parse_qs
from django.contrib.auth import get_user_model


class TokenAuthMiddleware:
    """
    Middleware для аутентификации WebSocket через JWT токен в URL.
    """

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):

        from django.contrib.auth.models import AnonymousUser
        from rest_framework_simplejwt.tokens import AccessToken

        query_string = scope.get('query_string', b'').decode('utf-8')

        query_params = parse_qs(query_string)

        token = query_params.get('token', [None])[0]

        if token:
            try:
                access_token = AccessToken(token)
                user_id = access_token['user_id']

                user = await self.get_user(user_id)
                if user and not isinstance(user, AnonymousUser):
                    scope['user'] = user
                else:
                    scope['user'] = AnonymousUser()
            except Exception as e:
                scope['user'] = AnonymousUser()
        else:
            scope['user'] = AnonymousUser()

        return await self.app(scope, receive, send)

    @staticmethod
    async def get_user(user_id):
        from django.contrib.auth.models import AnonymousUser
        User = get_user_model()
        try:
            return await User.objects.aget(id=user_id)
        except User.DoesNotExist:
            return AnonymousUser()