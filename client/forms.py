from .models import client, Comments, ClientFiles
from django import forms

class AddClientForm(forms.ModelForm):
    class Meta:
        model = client
        fields = [
            'name',
            'email',
            'description',
        ]

class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = [
            'content'
        ]

class AddFileForm(forms.ModelForm):
    class Meta:
        model = ClientFiles
        fields = [
            'file'
        ]