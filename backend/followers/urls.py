from django.urls import path

from followers import views

urlpatterns = [
    path('', views.FollowersApiView.as_view(), name="get all followers"),
    path('<str:foreign_author_id>', views.FollowersForeignApiView.as_view(), name="foreign and followers"),


]
