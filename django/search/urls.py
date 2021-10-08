from django.urls import path
from . import views

app_name = 'search'

urlpatterns = [
    path('post/', views.PostList.as_view(), name='post'),
    # path('post/advanced', views.PostList.as_view(), name='advanced'),
    path('account/', views.AccountList.as_view(), name='account'),
]
