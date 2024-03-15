from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView

# Create your views here.

class CustomLoginView(LoginView):
    fields = ['email', 'password']
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('todo:task-list')


