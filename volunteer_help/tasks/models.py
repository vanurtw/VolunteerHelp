from django.db import models
from users.models import MyUser


class TaskStatusManager(models.Manager):
    def open(self):
        return self.filter(status='open')

    def in_progress(self):
        return self.filter(status='in_progress')

    def completed(self):
        return self.filter(status='completed')

    def canceled(self):
        return self.filter(status='canceled')

    def active(self):
        return self.filter(status__in=['open', 'in_progress'])


class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    date_creation = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

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
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
    )
    status = models.CharField(
        max_length=20,
        choices=CHOICES_STATUS,
        default=STATUS_OPEN
    )
    date_creation = models.DateField(auto_now_add=True)
    date_due = models.DateTimeField()

    objects = models.Manager()
    status_objects = TaskStatusManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'


class ResponseTask(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Ожидает'),
        ('accepted', 'Принят'),
        ('rejected', 'Отклонён'),
    )

    status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=20,
        default='pending'
    )
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='responses')
    volunteer = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    date_creation = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('task', 'volunteer')
        verbose_name = 'Отклик'
        verbose_name_plural = 'Отклики'
