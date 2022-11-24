from django.contrib import admin
from .models import Inbox

class InboxAdmin(admin.ModelAdmin):
    filter_horizontal = ('posts', 'comments', 'likes', 'follow_requests',)

admin.site.register(Inbox, InboxAdmin)