
from django.db.models import (Model, CharField, URLField, TextChoices, TextField,
ForeignKey, CASCADE, IntegerField, DateTimeField,BooleanField
)
from django.forms import ImageField
# Create your models here.
class Author(Model):
    type =CharField(blank=False, null=False, default="author", max_length=200,)
    id = URLField(primary_key=True, editable=False)
    host = URLField(blank=True)
    displayName = CharField(max_length=200, blank=False, null=False)
    url = URLField(blank=True)
    github = URLField( blank=True)
    #profileImage = ImageField(blank=True, null=True)
