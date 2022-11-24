
from django.db.models import (Model, CharField, URLField, TextChoices, TextField,
ForeignKey, CASCADE, IntegerField, DateTimeField,BooleanField, ManyToManyField, UUIDField
)
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

    def create_user_uuid(self, displayName,  password=None, uuid=None):
        """Create an author with the provided display name, password, and uuid"""
        if displayName is None:
            raise TypeError('Users must have a username')
        

        user = self.model(displayName=displayName, uuid=uuid)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, displayName, password):
        """
        Create and return a `User` with superuser (admin) permissions.
        """
        host = 'https://cs404-project.herokuapp.com/'         # temporary solution...need to figure out a way to get host later on
        uuid = uuid4()
        url = host + 'service/authors/' + uuid.hex
        user = self.create_user_uuid(displayName, password, uuid)
        user.is_staff = True
        user.is_superuser = True
        user.host = host
        user.url = url
        user.id = url
        user.save(using=self._db)

        return user

class Author(AbstractBaseUser, PermissionsMixin):
    type =CharField(blank=False, null=False, default="author", max_length=200,)
    uuid = UUIDField(primary_key=True, blank=True, default=uuid4)
    id = URLField(blank=True, null=True)
    host = URLField(blank=True, null=True)
    displayName = CharField(max_length=200, blank=False, null=False, unique=True)
    url = URLField(blank=True)
    github = URLField( blank=True)
    profileImage = URLField(blank=True, default='')
    followers = ManyToManyField('self', blank=True, symmetrical=False)
    is_active = BooleanField(default=True)
    is_staff = BooleanField(default=False)
    is_superuser = BooleanField(default=False)

    objects = AuthorManager()

    USERNAME_FIELD = 'displayName'
    
    def __str__(self):
        return self.displayName
