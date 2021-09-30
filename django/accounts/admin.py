from django.contrib import admin
from .models import CustomUser

# Register your models here.
class CustomUserAdmin(admin.ModelAdmin):
    fields = ['username', 'email', 'is_superuser', 'description', 'photo']
    list_display = ('id', 'username', 'email', 'is_superuser', 'description', 'photo')

admin.site.register(CustomUser, CustomUserAdmin)
