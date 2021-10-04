"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.contrib.staticfiles.urls import static
from . import settings
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('timeline.urls')),
    path('', include('dm.urls')),
    path('accounts/email/', RedirectView.as_view(pattern_name='timeline:index')),
    path('accounts/inactive/', RedirectView.as_view(pattern_name='timeline:index')),
    path('accounts/password/change/', RedirectView.as_view(pattern_name='timeline:index')),
    path('accounts/confirm-email/', RedirectView.as_view(pattern_name='timeline:index')),
    re_path(r'^accounts/confirm-email/[^/]+/', RedirectView.as_view(pattern_name='timeline:index'), kwargs=None),
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('accounts.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
