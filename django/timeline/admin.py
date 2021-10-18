from django.contrib import admin
from .models import Post, Apply, Comment, CommentReply, Notification, Category

# Register your models here.


class PostAdmin(admin.ModelAdmin):
    fields = ['author', 'category', 'title', 'text', 'photo', 'is_recruited',
              'restriction', 'deadline', 'capacity', 'state_control_type']
    list_display = ('id', 'category', 'title', 'author', 'text', 'photo',
                    'is_recruited', 'restriction', 'deadline', 'capacity', 'created_at', 'updated_at', 'state_control_type')


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

class CategoryAdmin(admin.ModelAdmin):
    fields = ["parent", "display", "depth", "default_img"]
    list_display = ('id', "parent", "display", "depth", "default_img")


admin.site.register(Post, PostAdmin)
admin.site.register(Apply, ApplyAdmin)
admin.site.register(Notification)
admin.site.register(Comment, CommentAdmin)
admin.site.register(CommentReply, CommentReplyAdmin)
admin.site.register(Category, CategoryAdmin)
