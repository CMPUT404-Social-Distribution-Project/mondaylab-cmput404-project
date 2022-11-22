from django.contrib import admin
from django.contrib.auth.hashers import make_password
from backend.utils import remote_author_exists, display_name_exists, get_uuid_from_id
from author.serializers import AuthorSerializer
from .utils import authenticated_GET
from .models import Node

def create_node_authors(modeladmin, request, queryset):
    all_remote_authors = list()
    for node in queryset:
        node_authors_endpoint = f"{node.host}authors/"
        res = authenticated_GET(node_authors_endpoint, node)
        if (res.status_code == 200):
            all_remote_authors.extend(res.json()["items"])

    for remote_author in all_remote_authors:
        if not remote_author_exists(remote_author["id"]):
            if display_name_exists(remote_author["displayName"]):
                remote_author["displayName"] = remote_author["displayName"]+':'+remote_author["host"]
            
            remote_author["followers"] = []
            author_serializer = AuthorSerializer(data=remote_author)

            if author_serializer.is_valid():
                
                author_serializer.save(
                        uuid=get_uuid_from_id(remote_author["id"]),
                        id=remote_author.get("id"),
                        password=make_password(remote_author["displayName"]+"password")
                        )

class NodeAdmin(admin.ModelAdmin):
    actions = [create_node_authors]

admin.site.register(Node, NodeAdmin)
