from django.db import models
from .user import User

class Profile(models.Model):
    """
    this is model for profile information of user
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email