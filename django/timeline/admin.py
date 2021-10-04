from django.contrib import admin
from .models import Post, Apply

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    fields = ['text', 'title', 'photo', 'is_recruited', 'recruitment_conditions', 'capacity']
    list_display = ('id', 'title', 'author', 'text', 'photo', 'created_at', 'is_recruited', 'recruitment_conditions', 'capacity', 'created_at', 'updated_at')


class ApplyAdmin(admin.ModelAdmin):
    fields = ['is_member']
    list_display = ('id', 'is_member', 'post', 'user')

admin.site.register(Post, PostAdmin)
admin.site.register(Apply, ApplyAdmin)
