"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from rest_framework import routers
from post import views
from author.views import UserViewSet
from auth.views import LoginViewSet, RegistrationViewSet, RefreshViewSet
#################swagger start####################
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
schema_view = get_schema_view(
    openapi.Info(
        title="Cmput 404 peoject",
        default_version="v1.0.0", 
        description="temp",  
    ),
    public=True,
)
#################swagger end ####################
urlpatterns = [
    path('admin/', admin.site.urls),
    path('service/authors/', include("author.urls")),
    path('service/authors/<str:author_id>/posts/', include("post.urls")),
    path('service/authors/<str:author_id>/posts/<str:post_id>', include("post.urls")),
    path('service/', include(('backend.routers', 'backend'), namespace='backend-api')),
    path('service/authors/<str:author_id>/posts/<str:post_id>/comments/', include("comments.urls")),
    ##############swagger start###########
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    #################swagger end ####################
]
