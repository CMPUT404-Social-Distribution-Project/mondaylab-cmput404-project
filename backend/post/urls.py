from django.urls import path

from post import views

urlpatterns = [
    path('', views.PostsApiView.as_view(), name="create new post"),
    path('<str:post_id>', views.PostApiView.as_view(), name="individual post"),
    path('<str:post_id>/image', views.PostImageApiView.as_view(), name="individual post"),
]
