from celery import shared_task
from todo.models import Task


@shared_task
def deleteTask():
    Task.objects.filter(done=True).delete()
