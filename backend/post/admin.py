from django.contrib import admin
from .models import Post

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'published', 'author', 'authors_host']

    @admin.display(ordering="author__host", description="Author's Host")
    def authors_host(self, obj):
        return obj.author.host

admin.site.register(Post, PostAdmin)
