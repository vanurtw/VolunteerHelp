from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import UserProfileSerializer


def user_registration_docs():
    return swagger_auto_schema(
        operation_summary='Регистрация пользователя',
        operation_description='''
        Регистрация нового пользователя, возвращается пара токенов и данные о пользователе
        ''',
        tags=['Аутентификация и пользователи'],
        responses={
            201: openapi.Response(
                description="Успешная регистрация",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "refresh": openapi.Schema(
                            title="token",
                            type=openapi.TYPE_STRING,
                        ),
                        "access": openapi.Schema(
                            title="token",
                            type=openapi.TYPE_STRING,
                        ),
                        "user": openapi.Schema(
                            title="user",
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "id": openapi.Schema(
                                    title="id",
                                    type=openapi.TYPE_INTEGER
                                ),
                                "username": openapi.Schema(
                                    title="username",
                                    type=openapi.TYPE_STRING
                                ),
                                "status": openapi.Schema(
                                    title="status",
                                    type=openapi.TYPE_STRING
                                ),
                                "email": openapi.Schema(
                                    title="email",
                                    type=openapi.TYPE_STRING
                                )
                            }
                        )
                    }
                )

            ),
            400: openapi.Response(
                description='Ошибка валидации',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'field': openapi.Schema(
                            title='error',
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_STRING)
                        )
                    }
                )

            )
        }

    )


def user_profile_get_docs():
    return swagger_auto_schema(
        operation_summary='Получение своего профиля',
        operation_description='''
        Получение профиля пользователя.
        
        Доступно только для авторизованных
        Возвращает профиль.
        ''',
        tags=['Аутентификация и пользователи'],
        responses={
            200: openapi.Response(
                description='Успешный ответ',
                schema=UserProfileSerializer
            ),
            401: openapi.Response(
                description="Ошибка авторизации",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_STRING)
                        )
                    }
                )
            )
        }
    )


def user_profile_patch_docs():
    return swagger_auto_schema(
        operation_summary='Обновление своего профиля',
        operation_description='''
        Обновление профиля пользователя.
        Доступно только для авторизованных.
        ''',
        tags=['Аутентификация и пользователи'],
        responses={
            200: openapi.Response(
                description='Успешное обновление',
                schema=UserProfileSerializer
            ),
            400: openapi.Response(
                description='Ошибка валидации',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'field': openapi.Schema(
                            title='error',
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_STRING)
                        )
                    }
                )

            ),
            401: openapi.Response(
                description="Ошибка авторизации",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_STRING)
                        )
                    }
                )
            )
        }
    )


def token_obtain_pair_docs():
    return swagger_auto_schema(
        operation_summary='Получение токенов(вход пользователя)',
        operation_description='''
        Принимает набор учетных данных пользователя и возвращает пару веб-токенов JSON для доступа и обновления,
        подтверждающих подлинность этих учетных данных.
        refresh - долгоживущий токен
        access - короткоживущий токен
        ''',
        tags=['Аутентификация и пользователи'],
        responses={
            200: openapi.Response(
                description='Умпешный вход',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'refresh': openapi.Schema(
                            title='refresh token',
                            type=openapi.TYPE_STRING
                        ),
                        'access': openapi.Schema(
                            title='access token',
                            type=openapi.TYPE_STRING
                        )
                    }
                )
            ),
            400: openapi.Response(
                description='Ошибка валидации',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'field': openapi.Schema(
                            title='error',
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_STRING)
                        )
                    }
                )

            )
        }

    )


def token_refresh_docs():
    return swagger_auto_schema(
        operation_summary='Обновление токенов',
        operation_description='''
        Принимает refresh токен и обновляет access токен
        ''',
        tags=['Аутентификация и пользователи'],
        responses={
            200: openapi.Response(
                description='Умпешное обновление',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'access': openapi.Schema(
                            title='access token',
                            type=openapi.TYPE_STRING
                        )
                    }
                )
            ),
            400: openapi.Response(
                description='Ошибка валидации',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'field': openapi.Schema(
                            title='error',
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_STRING)
                        )
                    }
                )

            )
        }

    )
