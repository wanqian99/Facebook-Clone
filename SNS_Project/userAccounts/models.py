from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# User Account model extended from Django User model
class UserAccount(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    image = models.ImageField(default='userAccounts/user.png',upload_to='profileImage',null=True, blank=True)
    phone_number = models.CharField(max_length=20 ,null=True, blank=True, unique=True)
    dob = models.DateField(null=True, blank=True)
    
    # returns user.username
    def __unicode__(self):
        return self.user.username