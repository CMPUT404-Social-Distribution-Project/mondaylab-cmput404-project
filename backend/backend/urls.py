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
from followers.views import TrueFriendApiView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('service/authors/', include("author.urls")),
    path('service/authors/<str:author_id>/posts/', include("post.urls")),
    path('service/authors/<str:author_id>/posts/<str:post_id>', include("post.urls")),
    path('service/', include(('backend.routers', 'backend'), namespace='backend-api')),
    path('service/authors/<str:author_id>/posts/<str:post_id>/comments/', include("comments.urls")),
    path('service/authors/<str:author_id>/followers/', include("followers.urls")),
    path('service/authors/<str:author_id>/friends/<str:foreign_author_id>', TrueFriendApiView.as_view(), name = "check if true friends"),
    path('service/authors/<str:author_id>/posts/<str:post_id>/likes', include("like.urls")),
]
