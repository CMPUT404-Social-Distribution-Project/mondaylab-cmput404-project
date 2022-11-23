from django.contrib import admin
from django.contrib.auth.hashers import make_password
from backend.utils import remote_author_exists, create_remote_like, get_author_uuid_from_id, get_post_uuid_from_id, create_remote_post, create_remote_comment, create_remote_author, get_comment_uuid_from_id
from author.serializers import AuthorSerializer
from post.serializers import PostSerializer
from comments.serializers import CommentsSerializer
from .utils import authenticated_GET, getNodeRemoteAuthors
from .models import Node

def create_node_authors(modeladmin, request, queryset):
    all_remote_authors = list()
    for node in queryset:
        res = getNodeRemoteAuthors(node)
        all_remote_authors.extend(res)

    for remote_author in all_remote_authors:
        if not remote_author_exists(remote_author["id"]):
            try:
                create_remote_author(remote_author)
                remote_author_uuid = get_author_uuid_from_id(remote_author["id"])
                
                # create author's likes
                node_author_likes_endpoint = f"{node.host}authors/{remote_author_uuid}/liked"
                res = authenticated_GET(node_author_likes_endpoint, node) 
                remote_author_likes = res.json().get("items")
                if res.status_code == 200 and remote_author_likes:
                    for remote_author_like in remote_author_likes:
                        create_remote_like(remote_author_like)
            except Exception as e:
                print("Could not create remote author locally.", e)

def create_node_posts(modeladmin, request, queryset):
    for node in queryset:
        node_authors = getNodeRemoteAuthors(node)

        for remote_author in node_authors:
            remote_author_uuid = get_author_uuid_from_id(remote_author["id"])
            # make sure author exists/ create it if it doesn't
            if not remote_author_exists(remote_author["id"]):
                create_remote_author(remote_author)

            # Once author exists, we try to fetch to the remote node author's posts endpoint
            # to create it's posts locally
            node_posts_endpoint = f"{node.host}authors/{remote_author_uuid}/posts"
            res = authenticated_GET(node_posts_endpoint, node)
            if (res.status_code == 200):
                try:
                    remote_author_posts = res.json().get("items")
                    if remote_author_posts:
                        for remote_post in remote_author_posts:
                            remote_post_uuid = get_post_uuid_from_id(remote_post["id"])
                            remote_post = create_remote_post(remote_post, remote_author)

                            #TODO: If one of these points fail the rest won't get created
                            # e.g. if creating comments fails, then creating the likes won't happen.
                            # Maybe need separate try-catch clauses for each??
                            # create it's comments as well
                            node_post_comment_endpoint = f"{node.host}authors/{remote_author_uuid}/posts/{remote_post_uuid}/comments"
                            res = authenticated_GET(node_post_comment_endpoint, node)
                            remote_post_comments = res.json().get("comments")
                            if res.status_code == 200 and remote_post_comments:
                                for remote_comment in remote_post_comments:
                                    create_remote_comment(remote_comment)
                                    remote_comment_uuid = get_comment_uuid_from_id(remote_comment["id"])

                                    # create comment's likes
                                    node_likes_comment_endpoint = f"{node.host}authors/{remote_author_uuid}/posts/{remote_post_uuid}/comments/{remote_comment_uuid}/likes"
                                    res = authenticated_GET(node_likes_comment_endpoint, node) 
                                    remote_comment_likes = res.json().get("items")
                                    if res.status_code == 200 and remote_comment_likes:
                                        for remote_comment_like in remote_comment_likes:
                                            create_remote_like(remote_comment_like)

                            # create post's likes
                            node_likes_endpoint = f"{node.host}authors/{remote_author_uuid}/posts/{remote_post_uuid}/likes"
                            res = authenticated_GET(node_likes_endpoint, node) 
                            remote_post_likes = res.json().get("items")
                            if res.status_code == 200 and remote_post_likes:
                                for remote_post_like in remote_post_likes:
                                    create_remote_like(remote_post_like)

                except Exception as e:
                    print("Could not create remote post locally.", e)
            else:
                print("Failed to retrieve node posts.")

def create_node_objects(modeladmin, request, queryset):
    create_node_posts(modeladmin, request, queryset)
    create_node_authors(modeladmin, request, queryset)


class NodeAdmin(admin.ModelAdmin):
    actions = [create_node_authors, create_node_posts, create_node_objects]

admin.site.register(Node, NodeAdmin)
