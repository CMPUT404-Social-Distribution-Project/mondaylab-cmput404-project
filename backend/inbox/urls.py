from django.urls import path

from inbox import views

urlpatterns = [
    path("", views.InboxApiView.as_view(), name="retrieving an inbox")

]


