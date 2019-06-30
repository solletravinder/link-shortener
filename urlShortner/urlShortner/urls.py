"""urlShortner URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from customShortener import views
from rest_framework import routers
router = routers.DefaultRouter()
router.register(r'', views.LinkShortenerAPIView, '')

urlpatterns = [
    re_path(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
    re_path(r'swagger/', views.schema_view),
    re_path(r'shorten/', views.short, name="short"),
    re_path(r'(?P<url>\w+)/', views.expand, name="expand"),
    # re_path(r'api/link_shorten/',views.link_shorten),
    # re_path(r'api/link_expander/',views.link_expander),
    re_path(r'api/', include(router.urls))
]
