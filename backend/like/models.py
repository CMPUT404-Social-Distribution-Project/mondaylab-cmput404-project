from django.db.models import (Model, URLField, CharField, ForeignKey,CASCADE)
from author.models import Author
# Create your models here.




class Like(Model):

    context = URLField(max_length=300)
    summary = CharField(max_length=300, blank=True)
    type = CharField(max_length=4, default="Like", editable=False)
    author = ForeignKey(Author, related_name='like',on_delete = CASCADE)
    object = URLField(max_length=300, null=True)
    
