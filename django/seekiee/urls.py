from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'seekiee'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('post/', views.CreatePostView.as_view(), name='post'),
    path('my_post/', views.MyPostView.as_view(), name='my_post'),
    path('post_detail/<int:pk>', views.DetailView.as_view(), name='post_detail'),
    path('post_delete/<int:pk>', views.DeleteView.as_view(), name='post_delete'),
]