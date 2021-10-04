from django.contrib import admin
from .models import CustomUser

# Register your models here.
class CustomUserAdmin(admin.ModelAdmin):
    fields = ['username', 'email', 'is_superuser', 'description', 'photo', 'school', 'age', 'github_id']
    list_display = ('id', 'username', 'email', 'is_superuser', 'description', 'photo', 'school', 'age', 'github_id')

admin.site.register(CustomUser, CustomUserAdmin)
