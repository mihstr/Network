from django.contrib.auth.models import AbstractUser
from django.db import models

# add additional models to represent details about posts, likes, and followers.
# python manage.py makemigrations
# python manage.py migrate 
class User(AbstractUser):
    pass
