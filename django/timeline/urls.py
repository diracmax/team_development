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
    path('<int:pk>/comment/delete',
         views.delete_comment, name="delete_comment"),
]
