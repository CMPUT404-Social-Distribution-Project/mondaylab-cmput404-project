from django.urls import path

from comments import views

urlpatterns = [
    path('', views.CommentsApiView.as_view(), name="main_comment"),
]