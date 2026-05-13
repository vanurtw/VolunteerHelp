from django.db import models
from users.models import MyUser


class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    date_creation = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Task(models.Model):
    STATUS_OPEN = 'open'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_COMPLETED = 'completed'
    STATUS_CANCELED = 'canceled'

    CHOICES_STATUS = [
        (STATUS_OPEN, 'открыта'),
        (STATUS_IN_PROGRESS, 'в работе'),
        (STATUS_COMPLETED, 'выполнена'),
        (STATUS_CANCELED, 'отменена'),
    ]
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='user_tasks')
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_tasks')
    address = models.CharField(max_length=255)
    latitude = models.FloatField(
        null=True,
        blank=True
    )
    longitude = models.FloatField(
        null=True,
        blank=True
    )
    status = models.CharField(
        max_length=20,
        choices=CHOICES_STATUS,
        default=STATUS_OPEN
    )
    date_creation = models.DateField(auto_now_add=True)
    date_due = models.DateTimeField()

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
