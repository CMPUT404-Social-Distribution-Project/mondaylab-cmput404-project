from django.urls import path

from like import views

urlpatterns = [
    path('', views.LikesPostApiView.as_view(), name="like post"),
]
