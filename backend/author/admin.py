from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django import forms
from .models import Author

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

class AuthorAdmin(UserAdmin):
    add_form = AuthorCreationForm
    form = AuthorChangeForm
    model = Author
    # display the fields of the Author
    list_display = ('displayName', 'uuid', 'id', 'is_staff', 'is_active')
    list_filter = ('displayName', 'uuid', 'id', 'is_staff', 'is_active')
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

    search_fields = ('displayName', 'uuid', 'id')
    ordering = ('displayName', 'uuid', 'id')
    readonly_fields = ('id', 'uuid')

admin.site.register(Author, AuthorAdmin)



