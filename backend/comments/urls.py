from django.urls import path

from comments import views

urlpatterns = [
    path('', views.CommentsApiView.as_view(), name="main_comment"),
    path('<str:comment_id>', views.CommentApiView.as_view(), name="get comment with id"),
]