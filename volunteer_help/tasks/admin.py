from django.contrib import admin
from .models import Category, Task, ResponseTask


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'user', 'status']
    list_display_links = ['id', 'title']
    list_filter = ['user', 'status']


@admin.register(ResponseTask)
class ResponseTaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'task', 'volunteer', 'status']
    list_display_links = ['id', 'task']
    list_filter = ['volunteer', 'status']
