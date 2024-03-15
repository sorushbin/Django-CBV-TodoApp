from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.views.generic import FormView
from .forms import RegisterForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import login
from django.shortcuts import redirect

# Create your views here.

class CustomLoginView(LoginView):
    fields = ['username', 'password']
    redirect_authenticated_user = True
    template_name= 'accounts/login.html'

    def get_success_url(self):
        return reverse_lazy('todo:task-list')


class CustomRegisterView(SuccessMessageMixin, FormView):
    template_name = 'accounts/register.html'
    redirect_authenticated_user = True
    form_class = RegisterForm
    success_url = reverse_lazy('login')
    success_message = 'Your account was created successfully.Please Login.'

    def form_valid(self, form):
        user = form.save()
        return super(CustomRegisterView, self).form_valid(form)
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('todo:task-list')
        return super(CustomRegisterView, self).get(*args, **kwargs)

    

