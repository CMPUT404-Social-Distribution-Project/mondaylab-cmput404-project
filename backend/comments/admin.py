from django.contrib import admin
from .models import Comment, CommentSrc

admin.site.register(Comment)
admin.site.register(CommentSrc)
