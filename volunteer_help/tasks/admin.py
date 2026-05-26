from django.contrib import admin
from .models import Category, Task, ResponseTask


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    pass


@admin.register(ResponseTask)
class ResponseTask(admin.ModelAdmin):
    pass
