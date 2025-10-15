from django import forms
from .models import Art


class ArtForm(forms.ModelForm):
    class Meta:
        model = Art
        fields = [
            'collection',
            'title',
            'medium',
            'year_created',
            'image',
            'width_cm',
            'height_cm',
            'physical_available',
            'physical_price',
            'digital_available',
            'digital_price',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Friendly labels/placeholders
        self.fields['title'].widget.attrs.update(
            {'placeholder': 'Title of artwork'}
        )
        self.fields['medium'].widget.attrs.update(
            {'placeholder': 'Oil on canvas'}
        )
        self.fields['year_created'].widget.attrs.update(
            {'placeholder': 'YYYY'}
        )
        self.fields['width_cm'].widget.attrs.update(
            {'placeholder': 'Width (cm)'}
        )
        self.fields['height_cm'].widget.attrs.update(
            {'placeholder': 'Height (cm)'}
        )
        # Add Bootstrap classes
        for name, field in self.fields.items():
            css = field.widget.attrs.get('class', '')
            # checkbox fields should use form-check-input, not form-control
            if name in ('physical_available', 'digital_available'):
                field.widget = forms.CheckboxInput()
                field.widget.attrs.update(
                    {'class': (css + ' form-check-input').strip()}
                )
            elif name == 'image':
                field.widget.attrs.update(
                    {'class': (css + ' form-control-file').strip()}
                )
            else:
                field.widget.attrs.update(
                    {'class': (css + ' form-control').strip()}
                )
        # Make price inputs slightly smaller
        if 'physical_price' in self.fields:
            self.fields['physical_price'].widget.attrs.update(
                {'style': 'max-width:200px;'}
            )
        if 'digital_price' in self.fields:
            self.fields['digital_price'].widget.attrs.update(
                {'style': 'max-width:200px;'}
            )
