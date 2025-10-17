from django import forms
from .models import ArtistProfile, Contact


class ArtistProfileForm(forms.ModelForm):
    class Meta:
        model = ArtistProfile
        fields = ('name', 'email', 'phone_number', 'bio', 'image')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            css = field.widget.attrs.get('class', '')
            if name == 'image':
                field.widget.attrs.update(
                    {'class': (css + ' form-control-file').strip()}
                )
            else:
                field.widget.attrs.update(
                    {'class': (css + ' form-control').strip()}
                )

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = (
            'address_line_1',
            'address_line_2',
            'city',
            'zip_code',
            'phone',
            'email',
            'opening_hours',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            css = field.widget.attrs.get('class', '')
            field.widget.attrs.update(
                {'class': (css + ' form-control').strip()}
            )
