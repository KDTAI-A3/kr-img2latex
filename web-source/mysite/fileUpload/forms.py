from django import forms
from .models import ImageModel


class ImageModelForm(forms.ModelForm):
    class Meta:
        model = ImageModel
        fields = ['files','desc']

