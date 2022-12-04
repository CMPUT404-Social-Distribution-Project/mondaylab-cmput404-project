from datetime import date

from django import forms
from django.contrib.admin.models import ADDITION, CHANGE, DELETION, LogEntry
from django.contrib.admin.options import (
    HORIZONTAL,
    VERTICAL,
    ModelAdmin,
    TabularInline,
    get_content_type_for_model,
)
from django.contrib.admin.sites import AdminSite
from django.contrib.admin.widgets import (
    AdminDateWidget,
    AdminRadioSelect,
    AutocompleteSelect,
    AutocompleteSelectMultiple,
)
from django.contrib.auth.models import User
from django.db import models
from django.forms.widgets import Select
from django.test import SimpleTestCase, TestCase
from django.test.utils import isolate_apps


from .models import Node
from post.models import Post

class MockRequest:
    pass


class MockSuperUser:
    def has_perm(self, perm, obj=None):
        return True


request = MockRequest()
request.user = MockSuperUser()


class ModelAdminTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.node = Node.objects.create(
            host="http://localhost:8000",
            username='team1',
            password='123456789',
            team=1111
        )

    def setUp(self):
        self.site = AdminSite()

    def test_modeladmin_str(self):
        ma = ModelAdmin(Node, self.site)
        self.assertEqual(str(ma), "node.ModelAdmin")

    def test_default_attributes(self):
        ma = ModelAdmin(Node, self.site)
        self.assertEqual(ma.actions, ())
        self.assertEqual(ma.inlines, ())

    # form/fields/fieldsets interaction ##############################

    def test_default_fields(self):
        ma = ModelAdmin(Node, self.site)
        self.assertEqual(
            list(ma.get_form(request).base_fields), ["host", "username", "password", "team"]
        )
        self.assertEqual(list(ma.get_fields(request)), ["host", "username", "password", "team"])
        self.assertEqual(
            list(ma.get_fields(request, self.node)), ["host", "username", "password", "team"]
        )
        self.assertIsNone(ma.get_exclude(request, self.node))

    def test_default_fieldsets(self):
        # fieldsets_add and fieldsets_change should return a special data structure that
        # is used in the templates. They should generate the "right thing" whether we
        # have specified a custom form, the fields argument, or nothing at all.
        #
        # Here's the default case. There are no custom form_add/form_change methods,
        # no fields argument, and no fieldsets argument.
        ma = ModelAdmin(Node, self.site)
        self.assertEqual(
            ma.get_fieldsets(request),
            [(None, {"fields": ["host", "username", "password", "team"]})],
        )
        self.assertEqual(
            ma.get_fieldsets(request, self.node),
            [(None, {"fields": ["host", "username", "password", "team"]})],
        )




