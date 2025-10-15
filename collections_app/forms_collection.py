from django import forms
from .models import Collection


class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ['artist', 'name', 'description', 'cover_image']
        widgets = {
            'artist': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3}
            ),
            'cover_image': forms.ClearableFileInput(
                attrs={'class': 'form-control-file'}
            ),
        }
