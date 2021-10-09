from django.urls import path
from . import views

app_name = 'timeline'

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('delete/<int:pk>/', views.delete, name='delete'),
    path('<int:pk>/', views.detail, name='detail'),
    path('like/', views.like, name='like'),
    path('apply/', views.apply, name='apply'),
    path('accept/<int:post_id>/<int:user_id>/', views.accept, name='accept'),
    path('update/<int:pk>/', views.update, name='update'),
    path('<int:pk>/comment', views.comment, name="comment"),
    path('<int:pk>/comment/update', views.update_comment, name="update_comment"),
    path('comment/<int:pk>/list',
         views.comment_reply_list, name="comment_reply_list"),
    path('<int:pk>/comment/delete',
         views.delete_comment, name="delete_comment"),
    path('comment/<int:pk>/reply',
         views.comment_reply, name="comment_reply"),
    path('comment/<int:pk>/update',
         views.update_comment_reply, name="update_comment_reply"),
    path('comment/<int:pk>/delete',
         views.delete_comment_reply, name="delete_comment_reply"),
]
