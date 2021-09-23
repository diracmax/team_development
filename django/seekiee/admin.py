from django.contrib import admin
from .models import Categories, Posts

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
	list_display = ('id', 'title')
	list_display_links = ('id', 'title')


class PostAdmin(admin.ModelAdmin):
	list_display = ('id', 'title')
	list_display_links = ('id', 'title')


admin.site.register(Categories, CategoryAdmin)
admin.site.register(Posts, PostAdmin)