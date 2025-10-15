from django.db import models
from cloudinary.models import CloudinaryField


class Exhibition(models.Model):

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    STATUS_CHOICES = (
        ('upcoming', 'Upcoming'),
        ('ongoing', 'Ongoing'),
        ('finished', 'Finished'),
        ('cancelled', 'Cancelled'),
    )
    status = models.CharField(
        max_length=16, choices=STATUS_CHOICES, default='upcoming'
    )
    location = models.CharField(max_length=255, blank=True)
    cover_image = CloudinaryField(resource_type='image', blank=True, null=True)

    def __str__(self):
        return self.title


class ExhibitionArt(models.Model):

    exhibition = models.ForeignKey(
        Exhibition, on_delete=models.CASCADE, related_name='exhibition_arts'
    )
    art = models.ForeignKey(
        'collections_app.Art',
        on_delete=models.CASCADE,
        related_name='exhibitions',
    )

    class Meta:
        unique_together = ('exhibition', 'art')

    def __str__(self):
        return f"{self.exhibition.title} - {self.art.title}"
