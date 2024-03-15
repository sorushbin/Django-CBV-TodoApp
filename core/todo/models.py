from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

user = get_user_model()

class Task(models.Model):

    user = models.ForeignKey(user, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    description = models.TextField()
    done = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

