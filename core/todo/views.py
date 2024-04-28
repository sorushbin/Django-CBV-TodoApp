from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.views.generic.list import ListView
from .models import Task
from accounts.models import Profile
from .forms import TaskEditForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .tasks import deleteTask

class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = "tasks"
    template_name = "todo/list_task.html"

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user.id)


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    fields = ["title"]
    success_url = reverse_lazy("todo:task-list")

    def form_valid(self, form):
        form.instance.user = Profile.objects.get(user=self.request.user)
        return super(TaskCreateView, self).form_valid(form)


class TaskEditView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskEditForm
    template_name = "todo/edit_task.html"
    success_url = reverse_lazy("todo:task-list")


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = "task"
    success_url = reverse_lazy("todo:task-list")


class TaskDoneView(LoginRequiredMixin, ListView):
    model = Task
    success_url = reverse_lazy("todo:task-list")

    def get(self, request, *args, **kwargs):
        task = Task.objects.get(pk=kwargs.get("pk"))
        task.done = True
        task.save()
        return redirect(self.success_url)



