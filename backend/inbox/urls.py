from django.urls import path

from inbox import views

urlpatterns = [
    path("", views.InboxApiView.as_view(), name="retrieving an inbox"),
    path("all/", views.InboxAllApiView.as_view(), name="check if follow display in inbox"),
    path("<str:foreign_author_id>/", views.InboxDeleteFRApiView.as_view(), name="delete follow request from author ID"),
]


