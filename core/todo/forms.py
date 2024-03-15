from django import forms
from .models import Task



class TaskEditForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control rounded-4",
                "name": "title",
                
            }
        ),
        label=''
    )
    
    class Meta:
        model = Task
        fields = ['title']
