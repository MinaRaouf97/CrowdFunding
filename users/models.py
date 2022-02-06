from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(
        max_length=11,
        validators=[RegexValidator('(01)[0-9]{9}',
                                   message="phone number is not valid")])
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)


def __str__(self):
    return self.user.username
