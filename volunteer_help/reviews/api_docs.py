from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .serializers import ReviewSerializer
from users.serializers import UserProfileSerializer


def get_review_received():
    return swagger_auto_schema(
        operation_summary='Получить отзывы которые оставили на меня',
        operation_description='''
        Получить озтзывы которые оставили на меня(пользователя)
        
        Доступно только для авторизованных пользователей
        ''',
        tags=['Отзывы'],
        responses={
            200: openapi.Response(
                schema=ReviewSerializer,
                description='Успешный ответ'
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
            ),
            403: openapi.Response(
                description="Доступ запрещен",
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


def get_review_given():
    return swagger_auto_schema(
        operation_summary='Получить отзывы которые оставили текущий пользователь',
        operation_description='''
        Получить озтзывы которые оставил текущий(авторизованный) пользователь

        Доступно только для авторизованных пользователей
        ''',
        tags=['Отзывы'],
        responses={
            200: openapi.Response(
                schema=ReviewSerializer,
                description='Успешный ответ'
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
            ),
            403: openapi.Response(
                description="Доступ запрещен",
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


def post_review_create():
    return swagger_auto_schema(
        operation_summary='Остввить отзыв',
        operation_description='''
        Оставить отзыв на пользователя по переданному ID(задачи)
        
        оствить отзыв можно только после статуса у задачи completed т.е.
        только после того как она будет выполнена.
        
        Доступно только для авторизованных пользователей.
        ''',
        tags=['Отзывы'],
        responses={
            201: openapi.Response(
                schema=ReviewSerializer,
                description='Успешный ответ'
            ),
            400: openapi.Response(
                description='Ошибка валидации',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_STRING)
                        )
                    }
                )
            ),
            404: openapi.Response(
                description='Не найдено',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='Объект не найден.'
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
            ),
            403: openapi.Response(
                description="Доступ запрещен",
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


def get_review():
    return swagger_auto_schema(
        operation_summary='Получить отзывы пользователя по его ID',
        operation_description='''
        Получить отзывы пользователя по его ID
        
        id пользователя
        
        Доступно только для авторизованных пользователей
        ''',
        tags=['Отзывы', 'Аутентификация и пользователи'],
        responses={
            200: openapi.Response(
                schema=ReviewSerializer,
                description='Успешный ответ'
            ),
            404: openapi.Response(
                description='Не найдено',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='Объект не найден.'
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
            ),
            403: openapi.Response(
                description="Доступ запрещен",
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


def delete_review_destroy():
    return swagger_auto_schema(
        operation_summary='Удалить отзыв по его ID',
        operation_description='''
        Удалить отзыв по его ID
        
        Доступно только для авторизованных
        ''',
        tags=['Отзывы'],
        responses={
            204: openapi.Response(
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'status': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example='ok'
                        )
                    }
                ),
                description='Успешное удаление'
            ),
            404: openapi.Response(
                description='Не найдено',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='Объект не найден.'
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
            ),
            403: openapi.Response(
                description="Доступ запрещен",
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


def get_user_profile():
    return swagger_auto_schema(
        operation_summary='Получить профиль пользователя по ID(пользователя)',
        operation_description='''
        Получить профиль пользователя по ID(пользователя)

        Доступно только для авторизованных
        ''',
        tags=['Отзывы', 'Аутентификация и пользователи'],
        responses={
            200: openapi.Response(
                schema=UserProfileSerializer,
                description='Успешный ответ'
            ),
            404: openapi.Response(
                description='Не найдено',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='Объект не найден.'
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
            ),
            403: openapi.Response(
                description="Доступ запрещен",
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
