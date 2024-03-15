from django.urls import path
from .views import (TaskListView, TaskCreateView, TaskDoneView, TaskEditView, TaskDeleteView)

app_name = 'todo'

urlpatterns =[
    path('', TaskListView.as_view(), name = 'task-list'),
    path('create/', TaskCreateView.as_view(), name='task-create'),
    path('done/<int:pk>/', TaskDoneView.as_view(), name='task-done'),
    path('edit/<int:pk>/', TaskEditView.as_view(), name='task-edit'),
    path('delete/<int:pk>/', TaskDeleteView.as_view(), name='task-delete'),
]