from django import forms
from .models import *


class DesignForm(forms.ModelForm):
    class Meta:
        model = Design
        fields = ['design_name', 'description', 'image', 'price', 'inserted_by', 'creator_id']