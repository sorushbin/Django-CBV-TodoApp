from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
import requests
from accounts.models import Profile
from .models import Task
from .forms import TaskEditForm





class WeatherMixin:
    @method_decorator(cache_page(20*60))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_weather_data(self):
        city_name = "tehran"
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid=e1176c2224faec7d17373814500b2fa7"
        response = requests.get(url)
        weather_data =  response.json()
        if 'main' in weather_data and 'temp' in weather_data['main']:
            weather_data['main']['temp_celsius'] = int(weather_data['main']['temp'] - 273.15)
        return weather_data

class TaskBaseView(WeatherMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['weather'] = self.get_weather_data()
        return context


class TaskListView(LoginRequiredMixin,TaskBaseView, ListView):
    model = Task
    context_object_name = "tasks"
    template_name = "todo/task_list.html"

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user.id)


class TaskCreateView(LoginRequiredMixin,TaskBaseView, CreateView):
    model = Task
    fields = ["title"]
    success_url = reverse_lazy("todo:task-list")

    def form_valid(self, form):
        form.instance.user = Profile.objects.get(user=self.request.user)
        return super(TaskCreateView, self).form_valid(form)


class TaskEditView(LoginRequiredMixin,TaskBaseView, UpdateView):
    model = Task
    form_class = TaskEditForm
    template_name = "todo/edit_task.html"
    success_url = reverse_lazy("todo:task-list")


class TaskDeleteView(LoginRequiredMixin,TaskBaseView, DeleteView):
    model = Task
    context_object_name = "task"
    success_url = reverse_lazy("todo:task-list")


class TaskDoneView(LoginRequiredMixin,TaskBaseView, ListView):
    model = Task
    success_url = reverse_lazy("todo:task-list")

    def get(self, request, *args, **kwargs):
        task = Task.objects.get(pk=kwargs.get("pk"))
        task.done = True
        task.save()
        return redirect(self.success_url)
