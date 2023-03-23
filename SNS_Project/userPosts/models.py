from django.db import models
from userAccounts.models import *

# Create your models here.

# UserPost models stores posts information
class UserPost(models.Model):
    # stores the text content
    content = models.CharField(max_length=10000)

    # stores the image if there is any, to media/postImage
    content_image = models.ImageField(max_length=255, upload_to='postImage', null=True, blank=True)

    # stores the uploaded time, which will be used when organizing posts on the home page
    timestamp = models.DateTimeField(auto_now=True)

    # stores the post's user, this field is a fk that links to the django User model
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")