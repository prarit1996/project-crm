from .models import Lead, Comments, LeadFiles
from django import forms

class AddLeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = [
            'name',
            'email',
            'description',
            'priority',
            'status'
        ]

class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = [
            'content'
        ]

class AddFileForm(forms.ModelForm):
    class Meta:
        model = LeadFiles
        fields = [
            'file'
        ]