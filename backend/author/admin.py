from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django import forms
from .models import Author
from node.models import Node
from post.models import Post
from post.serializers import PostSerializer
from node.utils import authenticated_GET
from operator import itemgetter
from django.http import JsonResponse
from django.core import serializers
from backend.utils import is_our_backend

class AuthorCreationForm(UserCreationForm):
    ''' Form for creating authors
    '''
    displayName = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput)

    class Meta:
        model = Author
        fields = ('displayName',)

class AuthorChangeForm(UserChangeForm):
    ''' For updating authors'''
    # make the password read only
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Author
        readonly_fields = ('id', 'uuid')
        fields = ('displayName', 'profileImage', 'github', 'is_active', 'is_superuser', 'password', 'id', 'uuid')

def get_posts_of_authors_followers(modeladmin, request, queryset):
    '''Retrieves and returns all the posts of the selected author's followers, in reverse published order'''
    posts_list = []
    for author in queryset:
        for follower in author.followers.all():
            if is_our_backend(follower.host):
                posts_queryset = Post.objects.filter(author=follower)
                posts_serializer = PostSerializer(posts_queryset, many=True)
                posts_list.extend(posts_serializer.data)
            else:
                try:
                    node = Node.objects.get(host__contains=follower.host)
                    res = authenticated_GET(f"{follower.id}/posts/", node)
                    if isinstance(res, str):
                        raise ValueError(res)
                    if res.status_code == 200:
                        remote_posts = res.json().get("items")
                        posts_list.extend(remote_posts)
                except Exception as e:
                    print(f"Something went wrong trying to fetch to node {node.host}. {e}")
                    continue

    result = {
        "type":"posts",
        "items": sorted(posts_list, key=itemgetter('published'), reverse=True)
    }
    return JsonResponse(result)

def allow_authors_into_site(modeladmin, request, queryset):
    '''Sets the selected author's is_active field to true, which allows them to access the site.'''
    queryset.update(is_active=True)

class AuthorAdmin(UserAdmin):
    actions = [get_posts_of_authors_followers, allow_authors_into_site]
    add_form = AuthorCreationForm
    form = AuthorChangeForm
    model = Author
    # display the fields of the Author
    list_display = ('displayName', 'id', 'host', 'is_staff', 'is_active')
    list_filter = ('displayName', 'id', 'host', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('displayName', 'password', 'profileImage', 'host', 'github', 'url', 'id', 'uuid', 'followers')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('displayName', 'profileImage', 'host', 'github', 'password', 'is_staff', 'is_active')
        }),
    )
    filter_horizontal = ('followers',)
    search_fields = ('displayName', 'uuid', 'id')
    ordering = ('displayName', 'uuid', 'id')
    readonly_fields = ('id', 'uuid')

admin.site.register(Author, AuthorAdmin)



