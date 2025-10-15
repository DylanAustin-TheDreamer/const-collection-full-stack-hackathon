from django.db import models
from cloudinary.models import CloudinaryField


class ArtistProfile(models.Model):
    # Unique ID (auto PK by Django)
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=30, blank=True)
    bio = models.TextField(blank=True)
    image = CloudinaryField(resource_type='image', blank=True, null=True)

    def __str__(self):
        return f"{self.name} <{self.email}>"

    class Meta:
        verbose_name = 'Artist Profile'
        verbose_name_plural = 'Artist Profiles'
