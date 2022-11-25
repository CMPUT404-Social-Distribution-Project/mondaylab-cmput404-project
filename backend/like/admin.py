from django.contrib import admin
from .models import Like

class LikeAdmin(admin.ModelAdmin):
    list_display = ['summary', 'author', 'authors_host', 'like_object']

    @admin.display(ordering="author__host", description="Author's Host")
    def authors_host(self, obj):
        return obj.author.host
    
    @admin.display(description="Object UUID Liked")
    def like_object(self, obj):
        return obj.object.split('posts/')[1]


admin.site.register(Like, LikeAdmin)
