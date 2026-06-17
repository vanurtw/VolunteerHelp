from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


def chat_messages_docs():
    return swagger_auto_schema(
        method='get',
        operation_summary='История сообщений',
        operation_description='''
        Получить историю сообщений по задаче.

        **Доступно только для:** авторизованных участников задачи (нуждающийся или назначенный волонтёр) 
        при статусе задачи `in_progress`.
        ''',
        tags=['Чат'],
        responses={
            200: 'Список сообщений',
            401: 'Не авторизован',
            403: 'Доступ запрещён',
            404: 'Задача не найдена'
        }
    )