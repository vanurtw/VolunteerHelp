from django.contrib import admin
from .models import MyUser

@admin.register(MyUser)
class MyUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'username', 'status']
    list_display_links = ['id', 'email']

    list_filter = ['status']
