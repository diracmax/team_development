from django.urls import path
from . import views
from .views import PostNotification, FollowNotification, RemoveNotification, MessageNotification

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
    path('<int:pk>/comment/delete',
         views.delete_comment, name="delete_comment"),
    path('notification/<int:notification_pk>/post/<int:object_pk>', PostNotification.as_view(), name='post-notification'),
    path('notification/<int:notification_pk>/message/<int:object_pk>', MessageNotification.as_view(), name='message-notification'),
    path('notification/<int:notification_pk>/follow/<int:object_pk>', FollowNotification.as_view(), name='follow-notification'),
    path('notification/delete/<int:notification_pk>', RemoveNotification.as_view(), name='notification-delete'),
]
