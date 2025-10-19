from django import forms
from .models import Exhibition


class ExhibitionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # When editing an existing instance, format time values to HH:MM
        # so the rendered input value doesn't include seconds.
        try:
            instance = getattr(self, 'instance', None)
            # only set initial values when the form is NOT bound to POST data
            if instance and not getattr(self, 'is_bound', False):
                st = getattr(instance, 'start_time', None)
                if st and 'start_time' in self.fields:
                    val = st.strftime('%H:%M')
                    # set field and form initial so rendering works
                    self.fields['start_time'].initial = val
                    self.initial['start_time'] = val
                et = getattr(instance, 'end_time', None)
                if et and 'end_time' in self.fields:
                    val = et.strftime('%H:%M')
                    self.fields['end_time'].initial = val
                    self.initial['end_time'] = val
                # set initial values for date inputs so edit form retains dates
                sd = getattr(instance, 'start_date', None)
                if sd and 'start_date' in self.fields:
                    iso = sd.isoformat()
                    self.fields['start_date'].initial = iso
                    self.initial['start_date'] = iso
                ed = getattr(instance, 'end_date', None)
                if ed and 'end_date' in self.fields:
                    iso = ed.isoformat()
                    self.fields['end_date'].initial = iso
                    self.initial['end_date'] = iso
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
