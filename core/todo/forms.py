from django import forms
from .models import Task



class TaskEditForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-control-lg",
                "name": "title",
                "placeholder": "enter the title",
            }
        ),
        label="",
    )

    class Meta:
        model = Task
        fields = ("title",)
