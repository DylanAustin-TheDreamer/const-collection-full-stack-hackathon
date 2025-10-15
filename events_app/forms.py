from django import forms
from .models import Exhibition


class ExhibitionForm(forms.ModelForm):
    class Meta:
        model = Exhibition
        fields = [
            'title',
            'description',
            'location',
            'status',
            'start_date',
            'end_date',
            'cover_image',
        ]

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 4}
            ),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'start_date': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'}
            ),
            'end_date': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'}
            ),
            'cover_image': forms.ClearableFileInput(
                attrs={'class': 'form-control-file'}
            ),
        }
