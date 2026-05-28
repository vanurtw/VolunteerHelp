from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Category
from .serializers import (
    CategorySerializer,
    TaskSerializer,

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
        operation_summary='Создание задачи',
        operation_description='''
        Создание задачи
        
        Доступно только для авторизованных и нуждающихся.
        '''
    )