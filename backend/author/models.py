
from django.db.models import (Model, CharField, URLField, TextChoices, TextField,
ForeignKey, CASCADE, IntegerField, DateTimeField,BooleanField, ManyToManyField, UUIDField
)
from django.forms import ImageField
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser, PermissionsMixin)
from uuid import uuid4


class AuthorManager(BaseUserManager):
    def create_user(self, displayName,  password=None, **extra_fields):
        """Create and return a User with a username and password."""
        if displayName is None:
            raise TypeError('Users must have a username')
        

        user = self.model(displayName=displayName, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, displayName, password):
        """
        Create and return a `User` with superuser (admin) permissions.
        """

        #TODO: Need to find a way to get host URL of the current server that this backend is being hosted on..
        # we can't just use 127.0.0.1, as we'll eventually have to host this on heroku or whatever.
        # Why do we need the host URL? so the super user (server admin) can have an Author that they can
        # use regularly, but will have additional powers for server administration needs. 
        user = self.create_user(displayName, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user

class Author(AbstractBaseUser, PermissionsMixin):
    type =CharField(blank=False, null=False, default="author", max_length=200,)
    uuid = UUIDField(primary_key=True, blank=True, default=uuid4, editable=False)
    id = URLField(blank=True, null=True, editable=False)
    host = URLField(blank=True, null=True)
    displayName = CharField(max_length=200, blank=False, null=False, unique=True)
    url = URLField(blank=True)
    github = URLField( blank=True)
    profileImage = URLField(blank=True, default='')
    followers = ManyToManyField('self', blank=True)
    is_active = BooleanField(default=True)
    is_staff = BooleanField(default=False, editable=False)
    is_superuser = BooleanField(default=False, editable=False)

    objects = AuthorManager()

    USERNAME_FIELD = 'displayName'
    
    def __str__(self):
        return self.displayName

