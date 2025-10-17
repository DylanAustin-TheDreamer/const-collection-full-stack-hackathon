from django import forms
from .models import Exhibition


class ExhibitionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # When editing an existing instance, format time values to HH:MM
        # so the rendered input value doesn't include seconds.
        try:
            if getattr(self, 'instance', None):
                st = getattr(self.instance, 'start_time', None)
                if st and 'start_time' in self.fields:
                    # set the field initial explicitly so it is used when
                    # rendering an unbound ModelForm with an instance
                    self.fields['start_time'].initial = st.strftime('%H:%M')
                et = getattr(self.instance, 'end_time', None)
                if et and 'end_time' in self.fields:
                    self.fields['end_time'].initial = et.strftime('%H:%M')
        except Exception:
            # defensive: if formatting fails, leave values as-is
            pass
    
    class Meta:
        model = Exhibition
        fields = [
            'title',
            'description',
            'location',
            'status',
            'start_date',
            'start_time',
            'end_date',
            'end_time',
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
            'start_time': forms.TimeInput(
                attrs={
                    'class': 'form-control',
                    'type': 'time',
                    'step': '60',
                    'title': 'HH:MM',
                    'placeholder': 'HH:MM',
                    'pattern': '[0-9]{2}:[0-9]{2}',
                }
            ),
            'end_date': forms.DateInput(
                attrs={'class': 'form-control', 'type': 'date'}
            ),
            'end_time': forms.TimeInput(
                attrs={
                    'class': 'form-control',
                    'type': 'time',
                    'step': '60',
                    'title': 'HH:MM',
                    'placeholder': 'HH:MM',
                    'pattern': '[0-9]{2}:[0-9]{2}',
                }
            ),
            'cover_image': forms.ClearableFileInput(
                attrs={'class': 'form-control-file'}
            ),
        }
