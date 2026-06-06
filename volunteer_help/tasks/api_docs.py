from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Category
from .serializers import (
    CategorySerializer,
    TaskSerializer,
    TaskCreateSerializer,
    ResponseTaskMySerializer,
    ResponseTaskSerializer

)


def categories_docs():
    return swagger_auto_schema(
        operation_summary='Получение категорий для задачи',
        operation_description='''
        Получение всех категорий, доступно только для авторизованных
        ''',
        tags=['Категории'],
        responses={
            200: openapi.Response(
                description='Успешный ответ',
                schema=CategorySerializer
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


def get_tasks_docs():
    return swagger_auto_schema(
        operation_summary='Получение задач с фильтрацией для волонтеров',
        operation_description='''
        Доступно только для авторизованных волонтеров.
        
        Получение задач с фильтрацией по 2 параметрам:
        
        radius - радиус поиска в км
        
        category - slug выбранной категории
        
        передаются в GET-параметрах запроса http://.....?radius=10&category=uborka
        ''',
        tags=['Задачи'],
        manual_parameters=[
            openapi.Parameter(
                'radius',
                openapi.IN_QUERY,
                description="Радиус поиска в км",
                type=openapi.TYPE_NUMBER,
                format='float',
            ),
            openapi.Parameter(
                'category',
                openapi.IN_QUERY,
                description="Фильтр по категории. Используй slug",
                type=openapi.TYPE_STRING,
            ),
        ],
        responses={
            200: openapi.Response(
                description='Успешный ответ',
                schema=TaskSerializer
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


def post_tasks_docs():
    return swagger_auto_schema(
        operation_summary='Создание задачи. Только для нуждающегося',
        operation_description='''
        Создание задачи
        
        Доступно только для авторизованных и нуждающихся.
        
        ''',
        request_body=TaskCreateSerializer,
        tags=['Задачи'],
        responses={
            201: openapi.Response(
                description='Успешное создание',
                schema=TaskSerializer
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
            400: openapi.Response(
                description='Ошибка валидации',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'field_error': openapi.Schema(
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


def get_detail_task():
    return swagger_auto_schema(
        operation_summary='Детальный просмотр задачи',
        operation_description='''
        Детальный просмотр задачи по ее ID
        
        Доступно только для авторизованныйх пользователей, как для волонтеров так и для нуждающихся
        ''',
        tags=['Задачи'],
        responses={
            200: openapi.Response(
                description='Успешный ответ',
                schema=TaskSerializer
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


def patch_detail_task():
    return swagger_auto_schema(
        operation_summary='Обновление задач(Только для статуса open). Только для нуждающегося',
        operation_description='''
        Обновление задач. Доступно только для авторизованных и нуждающихся
        ''',
        tags=['Задачи'],
        request_body=TaskCreateSerializer,
        responses={
            200: openapi.Response(
                description='Успешное обновление',
                schema=TaskSerializer
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


def delete_detail_task():
    return swagger_auto_schema(
        operation_summary='Удаление задачи(Только со статусом open). Только для нуждающегося',
        operation_description='''
        Удаление задачи.
        
        Доступно только для авторизованных нуждающихся.
        Удаляет только свои задачи со статусом open.
        ''',
        tags=['Задачи'],
        responses={
            204: openapi.Response(
                description='Успешное удаление',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Статус операции",
                            example="ok"
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


def get_my_tasks():
    return swagger_auto_schema(
        operation_summary='Получить мои задачи. Только для нуждающегося',
        operation_description='''
        Получить свои задачи. Доступно только для авторизованных нуждающихся.
        ''',
        tags=['Задачи'],
        responses={
            200: openapi.Response(
                description='Успешный ответ',
                schema=TaskSerializer
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


def post_task_respond():
    return swagger_auto_schema(
        operation_summary='Откликнуться на задачу. Только для волонтеров',
        operation_description='''
        Откликнуться на задачу. Только для волонтеров.
        
        После отклика, у нуждающегося появляется в разделе отклики, этот отклик т.е. 
        что волонтер откликнулся на эту задачу. Он может принять этот отклик или выбрать другого
        исполнителя задачи.
        ''',
        tags=['Отклики'],
        responses={
            201: openapi.Response(
                description="Успешная регистрация",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "succes": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Статус оперции",
                            example="True"
                        ),
                        "response_id": openapi.Schema(
                            title="response_id",
                            type=openapi.TYPE_INTEGER,
                        ),
                        "task_id": openapi.Schema(
                            title="task_id",
                            type=openapi.TYPE_INTEGER,
                        ),

                    }
                )

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
        }
    )


def delete_task_respond():
    return swagger_auto_schema(
        operation_summary='Отмена отклика на задачу только со статусом pending. Доступно только для волонтеров ',
        operation_description='''
        отмена отклика на задачу. ID - задачи
        
        Отклик отменится только если он не принят нуждающимся т.е. имеет статус pending
        ''',
        tags=['Отклики'],
        responses={
            204: openapi.Response(
                description='Успешное удаление',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Статус операции",
                            example="ok"
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


def get_task_my_response():
    return swagger_auto_schema(
        operation_summary='Все мои отклики. Доступно только для волонтеров',
        operation_description='''
        Получение всех моих откликов. 
        
        Доступно только для авторизованных волонтеров.
        ''',

        tags=['Отклики'],
        responses={
            200: openapi.Response(
                description='Успешный ответ',
                schema=ResponseTaskMySerializer
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


def get_task_response():
    return swagger_auto_schema(
        operation_summary='Получить все отклики на задачу. Только для нуждающихся',
        operation_description='''
        Получить все отклики на задачу. Только для авторизованных нуждающихся
        ''',
        tags=['Отклики'],
        responses={
            200: openapi.Response(
                description='Успешный ответ',
                schema=ResponseTaskSerializer
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


def post_task_accept_response():
    return swagger_auto_schema(
        operation_summary='Принять отклик на задачу. Доступно для нуждающихся',
        operation_description='''
        Принять выбранный отклик по переданному ID(отклика)
        
        Проверка на то что задача открыта для выполнения, после этого статус у всех откликах переходит в rejected
        за исключением выбранной у нее accepted.
        
        Статус задачи меняется на in_progress
        
        Доступно только для авторизованных нуждающихся
        ''',

        tags=['Отклики'],
        responses={
            200: openapi.Response(
                description='Успешное удаление',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "success": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Статус операции",
                            example="True"
                        ),
                        "task_id":openapi.Schema(
                            type=openapi.TYPE_INTEGER,
                            description="id задачи"
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

