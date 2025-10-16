from django.db import models
from cloudinary.models import CloudinaryField


class Collection(models.Model):

    artist = models.ForeignKey(
        'owner_app.ArtistProfile',
        on_delete=models.CASCADE,
        related_name='collections',
    )
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    # allow either image or video uploads for collection cover
    cover_image = CloudinaryField(resource_type='auto', blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.artist})"


class Art(models.Model):

    collection = models.ForeignKey(
        Collection, on_delete=models.CASCADE, related_name='arts'
    )
    title = models.CharField(max_length=200)
    medium = models.CharField(max_length=200, blank=True)
    year_created = models.IntegerField(null=True, blank=True)
    image = CloudinaryField(resource_type='image', blank=True, null=True)
    width_cm = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True
    )
    height_cm = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True
    )

    # Store-related fields
    physical_available = models.BooleanField(default=False)
    digital_available = models.BooleanField(default=False)
    physical_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    digital_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )

    def __str__(self):
        return f"{self.title} ({self.collection.name})"

    def clean(self):
        # ensure price is set if availability is true
        from django.core.exceptions import ValidationError

        errors = {}
        if self.physical_available and not self.physical_price:
            errors['physical_price'] = (
                'Set a physical price when physical_available is True.'
            )
        if self.digital_available and not self.digital_price:
            errors['digital_price'] = (
                'Set a digital price when digital_available is True.'
            )
        if errors:
            raise ValidationError(errors)
