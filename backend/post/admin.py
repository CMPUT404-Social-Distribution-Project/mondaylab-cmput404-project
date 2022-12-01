from django.contrib import admin
from .models import Post

class PostAdmin(admin.ModelAdmin):
    list_display = ['title_display', 'uuid' ,'published', 'author', 'id']
    search_fields = ('uuid', 'id')

    @admin.display(description="Title")
    def title_display(self, obj):
        if obj.title == "":
            return "empty title"
        else:
            return obj.title

    @admin.display(ordering="author__host", description="Author's Host")
    def authors_host(self, obj):
        if obj.author.host != None:
            return obj.author.host
        else:
            return ""

admin.site.register(Post, PostAdmin)
