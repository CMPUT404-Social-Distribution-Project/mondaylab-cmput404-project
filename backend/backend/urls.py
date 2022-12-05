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
import imp
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from post import views
from author.views import UserViewSet
from auth.views import LoginViewSet, RegistrationViewSet, RefreshViewSet
from followers.views import TrueFriendApiView, TrueFriendsApiView
from like.views import LikesPostApiView, AuthorLikedApiView, LikesCommentApiView
from node.views import AcceptConnectionFromRemote, getNode, getNodeAuthors, getNodePosts
from django.conf import settings
from django.conf.urls.static import static
from inbox.views import InboxApiView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Author/Authentication Endpoints (See routers.py in backend/ folder)
    path('service/', include(('backend.routers', 'backend'), namespace='authors')),

    # Post Endpoints
    path('service/authors/<str:author_id>/posts/', include("post.urls")),
    path('service/posts/', views.AllPostsApiView.as_view(), name="all-posts"),
    # Comment Endpoints
    path('service/authors/<str:author_id>/posts/<str:post_id>/comments/', include("comments.urls")),

    # Follower/Friend Endpoints
    path('service/authors/<str:author_id>/followers/', include("followers.urls")),
    path('service/authors/<str:author_id>/friends/', TrueFriendsApiView.as_view(), name = "get true friends"),
    path('service/authors/<str:author_id>/friends/<str:foreign_author_id>', TrueFriendApiView.as_view(), name = "check if true friends"),


    # Inbox Endpoints
    path("service/authors/<str:author_id>/inbox/",include("inbox.urls"), name="get all post from inbox"),
    path("service/authors/<str:author_id>/inbox", InboxApiView.as_view(), name="get all post from inbox"),

    # Like Endpoints
    path('service/authors/<str:author_id>/posts/<str:post_id>/likes/', LikesPostApiView.as_view(), name="post like"),
    path('service/authors/<str:author_id>/posts/<str:post_id>/comments/<str:comment_id>/likes/', LikesCommentApiView.as_view(), name="comment likes"),
    path('service/authors/<str:author_id>/liked', AuthorLikedApiView.as_view(), name="author like"),


    # Node enpoint
    path('service/node/<str:hostName>', AcceptConnectionFromRemote, name="connect to our server"),
    path('service/node/', getNode, name="retrieves node object"),
    path('service/node/authors/', getNodeAuthors, name="retrieves all authors from all nodes"),
    path('service/node/posts/', getNodePosts, name="retrieves all posts from all nodes"),


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

