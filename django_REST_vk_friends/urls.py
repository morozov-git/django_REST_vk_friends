"""
URL configuration for django_REST_vk_friends project.

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
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework import permissions
from rest_framework.schemas import get_schema_view


open_api_schema = get_schema_view(
        title='REST VK Friends',
        description='AOpenAPI Specification for Django REST VK Friends',
        version='1.0.0',
        permission_classes=(permissions.AllowAny,),
        public=True,
    )
swagger_template = TemplateView.as_view(template_name='swagger-ui.html', extra_context={'schema_url': 'openapi_schema'})

redoc_template = TemplateView.as_view(template_name='redoc.html', extra_context={'schema_url': 'openapi_schema'})


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('api/', include('users.urls')),
    path('api/friends/', include('friends.urls')),
    path('openapi/', open_api_schema, name='openapi_schema'),
    path('swagger-ui/', swagger_template, name='swagger-ui'),
    path('redoc/', redoc_template, name='redoc'),
]
