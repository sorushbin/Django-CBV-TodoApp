from django.db import models
from datetime import datetime
# Create your models here.


class Task(models.Model):

    user = models.ForeignKey("accounts.Profile", on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)
    done = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
