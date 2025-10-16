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
    cover_image = CloudinaryField(resource_type='image', blank=True, null=True)

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


# New Artwork Model for displaying price, size, and medium
class Artwork(models.Model):
    """
    Model representing an artwork with essential buyer information.
    This model includes fields for price, size, and medium to help buyers
    make informed purchasing decisions.
    """

    # Basic Information
    # Title of the artwork
    title = models.CharField(
        max_length=200,
        help_text="The name/title of the artwork"
    )
    
    # Artist Information
    # Foreign key to link artwork to an artist
    artist = models.ForeignKey(
        'owner_app.ArtistProfile',
        on_delete=models.CASCADE,
        related_name='artworks',
        help_text="The artist who created this artwork"
    )
    
    # Medium Information
    # The medium/materials used to create the artwork
    medium = models.CharField(
        max_length=200,
        blank=True,
        help_text="Medium used (e.g., Oil on Canvas, Acrylic, Watercolor, Digital, Mixed Media)"
    )
    
    # Size Information
    # Width of the artwork in centimeters
    width_cm = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Width of the artwork in centimeters"
    )
    
    # Height of the artwork in centimeters
    height_cm = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Height of the artwork in centimeters"
    )
    
    # Depth of the artwork in centimeters (for 3D artworks)
    depth_cm = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Depth of the artwork in centimeters (optional, for 3D works)"
    )
    
    # Price Information
    # Price of the artwork in the default currency
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Price of the artwork (in default currency)"
    )
    
    # Currency field to specify the currency of the price
    currency = models.CharField(
        max_length=3,
        default='USD',
        help_text="Currency code (e.g., USD, EUR, GBP)"
    )
    
    # Additional Information
    # Description of the artwork
    description = models.TextField(
        blank=True,
        help_text="Detailed description of the artwork"
    )
    
    # Year the artwork was created
    year_created = models.IntegerField(
        null=True,
        blank=True,
        help_text="Year the artwork was created"
    )
    
    # Image of the artwork
    image = CloudinaryField(
        resource_type='image',
        blank=True,
        null=True,
        help_text="Primary image of the artwork"
    )
    
    # Availability status
    is_available = models.BooleanField(
        default=True,
        help_text="Is the artwork available for purchase?"
    )
    
    # Featured artwork flag
    is_featured = models.BooleanField(
        default=False,
        help_text="Mark as featured artwork for homepage display"
    )
    
    # Timestamps
    # Date and time when the artwork was added to the system
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Date and time when artwork was added"
    )
    
    # Date and time when the artwork was last updated
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Date and time when artwork was last updated"
    )

    class Meta:
        # Order artworks by creation date (newest first)
        ordering = ['-created_at']
        # Add verbose names for admin interface
        verbose_name = 'Artwork'
        verbose_name_plural = 'Artworks'

    def __str__(self):
        """String representation of the artwork"""
        return f"{self.title} by {self.artist}"
    
    def get_size_display(self):
        """
        Returns a formatted string representation of the artwork size.
        Returns: String in format "Width x Height cm" or "Width x Height x Depth cm" for 3D works
        """
        if self.width_cm and self.height_cm:
            if self.depth_cm:
                # For 3D artworks, include depth
                return f"{self.width_cm} x {self.height_cm} x {self.depth_cm} cm"
            else:
                # For 2D artworks
                return f"{self.width_cm} x {self.height_cm} cm"
        return "Size not specified"
    
    def get_price_display(self):
        """
        Returns a formatted string representation of the price.
        Returns: String with currency symbol and price (e.g., "$1,250.00")
        """
        if self.price:
            # Format price with thousand separators
            return f"{self.currency} {self.price:,.2f}"
        return "Price not available"
    
    def clean(self):
        """
        Validate the model fields before saving.
        Ensures that if the artwork is available, it must have a price.
        """
        from django.core.exceptions import ValidationError
        
        errors = {}
        
        # If artwork is available for purchase, it must have a price
        if self.is_available and not self.price:
            errors['price'] = 'Price must be set when artwork is available for purchase.'
        
        # Ensure dimensions are positive values
        if self.width_cm is not None and self.width_cm <= 0:
            errors['width_cm'] = 'Width must be a positive value.'
        
        if self.height_cm is not None and self.height_cm <= 0:
            errors['height_cm'] = 'Height must be a positive value.'
        
        if self.depth_cm is not None and self.depth_cm <= 0:
            errors['depth_cm'] = 'Depth must be a positive value.'
        
        # Raise validation errors if any exist
        if errors:
            raise ValidationError(errors)
