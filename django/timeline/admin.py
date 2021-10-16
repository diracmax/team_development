from django.contrib import admin
from .models import Post, Apply, Comment, CommentReply, Notification

# Register your models here.


class PostAdmin(admin.ModelAdmin):
    fields = ['text', 'title', 'photo', 'is_recruited',
              'recruitment_conditions', 'capacity']
    list_display = ('id', 'title', 'author', 'text', 'photo', 'created_at',
                    'is_recruited', 'recruitment_conditions', 'capacity', 'created_at', 'updated_at')


class ApplyAdmin(admin.ModelAdmin):
    fields = ['is_member']
    list_display = ('id', 'is_member', 'post', 'user')


class CommentAdmin(admin.ModelAdmin):
    fields = ['text']
    list_display = ('id', 'author', 'post', 'text',
                    'created_at', 'updated_at')


class CommentReplyAdmin(admin.ModelAdmin):
    fields = ['text']
    list_display = ('id', 'author', 'parent', 'text',
                    'created_at', 'updated_at')


admin.site.register(Post, PostAdmin)
admin.site.register(Apply, ApplyAdmin)
admin.site.register(Notification)
admin.site.register(Comment, CommentAdmin)
admin.site.register(CommentReply, CommentReplyAdmin)
