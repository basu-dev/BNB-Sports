from django.db import models
from django.contrib import auth


# Create your models here.


class User(auth.models.User, auth.models.PermissionsMixin):
    def __str__(self):
        return self.username
class About(models.Model):
    body=models.TextField(default="This is about!!!")
class Topbrand(models.Model):
    name=models.CharField(max_length=50)
    logo=models.ImageField(upload_to="logos/",default="logos/default/brandlogo.png/")