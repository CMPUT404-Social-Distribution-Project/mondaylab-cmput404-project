from django.urls import path

from post import views

urlpatterns = [
    path('', views.PostsApiView.as_view(), name="main_comment"),
]