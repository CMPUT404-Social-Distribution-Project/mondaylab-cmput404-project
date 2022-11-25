from django.contrib import admin
from .models import Comment, CommentSrc


class CommentAdmin(admin.ModelAdmin):
    list_display = ['comment', 'published', 'author']

admin.site.register(Comment, CommentAdmin)
admin.site.register(CommentSrc)