from django import forms
from .models import Art, ArtVariant
from .models import Media


class MediaForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = [
            'file',
            'media_type',
            'hero',
            'second_section',
            'third_section',
            'caption',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Small UX tweaks
        if 'media_type' in self.fields:
            self.fields['media_type'].widget.attrs.update(
                {'class': 'form-select'}
            )
        # new homepage flags (checkboxes)
        for flag in ('hero', 'second_section', 'third_section'):
            if flag in self.fields:
                self.fields[flag].widget = forms.CheckboxInput()
                self.fields[flag].widget.attrs.update(
                    {'class': 'form-check-input'}
                )
        if 'caption' in self.fields:
            self.fields['caption'].widget.attrs.update(
                {'class': 'form-control'}
            )


class ArtForm(forms.ModelForm):
    # Per-medium fields for owner to set availability and price per format
    original_available = forms.BooleanField(required=False, initial=False)
    original_price = forms.DecimalField(
        required=False, max_digits=10, decimal_places=2
    )

    poster_available = forms.BooleanField(required=False, initial=False)
    poster_price = forms.DecimalField(
        required=False, max_digits=10, decimal_places=2
    )

    digital_available = forms.BooleanField(required=False, initial=False)
    digital_price = forms.DecimalField(
        required=False, max_digits=10, decimal_places=2
    )

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
            # new consolidated/store fields
            'price',
            'currency',
            'is_available',
            'is_featured',
            'depth_cm',
            'description',
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
        # new field placeholders
        if 'price' in self.fields:
            self.fields['price'].widget.attrs.update(
                {'placeholder': 'e.g. 1000.00'}
            )
        if 'currency' in self.fields:
            self.fields['currency'].widget.attrs.update(
                {'placeholder': 'USD'}
            )
        if 'depth_cm' in self.fields:
            self.fields['depth_cm'].widget.attrs.update(
                {'placeholder': 'Depth (cm) - optional'}
            )
        if 'description' in self.fields:
            # use a textarea for description if it's present on the form
            self.fields['description'].widget = forms.Textarea()
            self.fields['description'].widget.attrs.update(
                {
                    'placeholder': 'Short description',
                    'rows': 4,
                }
            )
        # Pre-populate per-medium variant fields when editing existing Art
        if self.instance and getattr(self.instance, 'pk', None):
            variants = {v.medium: v for v in self.instance.variants.all()}

            # original
            orig = variants.get(ArtVariant.ORIGINAL)
            if orig:
                self.fields['original_available'].initial = orig.is_available
                self.fields['original_price'].initial = orig.price

            # poster
            poster = variants.get(ArtVariant.POSTER)
            if poster:
                self.fields['poster_available'].initial = poster.is_available
                self.fields['poster_price'].initial = poster.price

            # digital
            digital = variants.get(ArtVariant.DIGITAL)
            if digital:
                self.fields['digital_available'].initial = digital.is_available
                self.fields['digital_price'].initial = digital.price
        # Add Bootstrap classes
        for name, field in self.fields.items():
            css = field.widget.attrs.get('class', '')
            # checkbox fields should use form-check-input, not form-control
            if name in ('is_available', 'is_featured'):
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
        # Ensure modern consolidated price field has a compact input
        if 'price' in self.fields:
            self.fields['price'].widget.attrs.update(
                {'style': 'max-width:200px;'}
            )
        if 'currency' in self.fields:
            self.fields['currency'].widget.attrs.update(
                {'style': 'max-width:120px;'}
            )

        # Style per-medium price inputs
        for key in (
            'original_price',
            'poster_price',
            'digital_price',
        ):
            if key in self.fields:
                self.fields[key].widget.attrs.update(
                    {'class': 'form-control', 'style': 'max-width:180px;'}
                )

        # Ensure per-medium checkboxes use form-check-input
        for key in (
            'original_available',
            'poster_available',
            'digital_available',
        ):
            if key in self.fields:
                self.fields[key].widget = forms.CheckboxInput()
                css = self.fields[key].widget.attrs.get('class', '')
                self.fields[key].widget.attrs.update(
                    {'class': (css + ' form-check-input').strip()}
                )

    def save(self, commit=True):
        # Save Art instance first
        art = super().save(commit=commit)

        # Helper to update/create variant
        def upsert_variant(medium_const, avail_field, price_field):
            avail = self.cleaned_data.get(avail_field, False)
            price = self.cleaned_data.get(price_field, None)
            variant, _ = ArtVariant.objects.get_or_create(
                art=art, medium=medium_const
            )
            variant.is_available = bool(avail)
            # allow None for price
            variant.price = price if price is not None else None
            # use art.currency as the variant currency by default
            variant.currency = getattr(art, 'currency', 'USD') or 'USD'
            variant.save()

        upsert_variant(
            ArtVariant.ORIGINAL, 'original_available', 'original_price'
        )
        upsert_variant(
            ArtVariant.POSTER, 'poster_available', 'poster_price'
        )
        upsert_variant(
            ArtVariant.DIGITAL, 'digital_available', 'digital_price'
        )

        # Derive overall Art.is_available from any variant being available
        any_avail = (
            ArtVariant.objects.filter(
                art=art, is_available=True
            ).exists()
        )
        if art.is_available != any_avail:
            art.is_available = any_avail
            # ensure change is saved when using commit=True
            if commit:
                art.save()

        return art
