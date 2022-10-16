from django.urls import path

from author import views

urlpatterns = [
    path('', views.AuthorsApiView.as_view(), name="author"),
    path('create/',views.AuthorApiView.as_view(), name="create_author"), #for test
    path('<str:author_id>/', views.AuthorApiView.as_view(), name="get_author"),
]
