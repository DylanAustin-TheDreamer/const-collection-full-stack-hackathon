"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from owner_app import views as owner_views
from collections_app import views as collections_views
from allauth.urls import path as allauth_path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('collections_app.urls')),
    path('events/', include('events_app.urls')),
    path('store/', include('store_app.urls')),
    path('owner/', include('owner_app.urls')),
    path('contact/', collections_views.contact, name='contact'),
    path('about/', owner_views.public_about, name='about'),

    path('accounts/', include('allauth.urls')),
]

# Serve static files during development and ensure Unity files are served
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0] if settings.STATICFILES_DIRS else None)
    # Development-only debug routes
    urlpatterns += [
        path('debug/tint-demo/', collections_views.tint_demo, name='tint_demo'),
    ]
