from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('edit/', views.edit, name='edit'),
    path('<int:pk>/', views.detail, name='detail'),
    path('<int:pk>/<str:query>', views.PostList.as_view(), name='posts'),
    path('quit/', views.quit, name='quit'),
    path('signup/', views.signup, name='signup'),
]
