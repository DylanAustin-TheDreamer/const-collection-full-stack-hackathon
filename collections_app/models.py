from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
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


# ============================================================================
# BASKET MODELS - Shopping cart functionality for purchasing artworks
# ============================================================================

class Basket(models.Model):
    """
    Shopping basket/cart model for storing user's selected artworks.
    Each user has one active basket that persists across sessions.
    
    Features:
    - Linked to authenticated users
    - Tracks creation and update times
    - Calculates total basket value
    - Supports multiple items
    """
    
    # User who owns this basket
    # Each user can have one basket
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='basket',
        help_text="The user who owns this basket"
    )
    
    # Timestamps
    # When the basket was first created
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When the basket was created"
    )
    
    # When the basket was last updated (item added/removed)
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="When the basket was last modified"
    )
    
    class Meta:
        verbose_name = 'Basket'
        verbose_name_plural = 'Baskets'
        ordering = ['-updated_at']
    
    def __str__(self):
        """String representation of the basket"""
        return f"Basket for {self.user.username}"
    
    def get_total_price(self):
        """
        Calculate the total price of all items in the basket.
        
        Returns:
            Decimal: Total price of all basket items
        """
        total = sum(item.get_subtotal() for item in self.items.all())
        return total
    
    def get_item_count(self):
        """
        Get the total number of items (considering quantities) in the basket.
        
        Returns:
            int: Total quantity of all items
        """
        return sum(item.quantity for item in self.items.all())
    
    def get_unique_item_count(self):
        """
        Get the number of unique items in the basket.
        
        Returns:
            int: Number of unique artworks in basket
        """
        return self.items.count()
    
    def clear(self):
        """
        Remove all items from the basket.
        Used after successful purchase or when user wants to clear basket.
        """
        self.items.all().delete()


class BasketItem(models.Model):
    """
    Individual item in a shopping basket.
    Represents an artwork that a user wants to purchase.
    
    Features:
    - Links artwork to basket
    - Tracks quantity (for prints/reproductions)
    - Stores price snapshot at time of adding (protects against price changes)
    - Calculates subtotal
    """
    
    # The basket this item belongs to
    basket = models.ForeignKey(
        Basket,
        on_delete=models.CASCADE,
        related_name='items',
        help_text="The basket containing this item"
    )
    
    # The artwork being purchased
    artwork = models.ForeignKey(
        Artwork,
        on_delete=models.CASCADE,
        related_name='basket_items',
        help_text="The artwork in this basket item"
    )
    
    # Quantity of this artwork (usually 1 for originals, can be >1 for prints)
    quantity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        help_text="Number of items (usually 1 for original artworks)"
    )
    
    # Price snapshot - stores the price at the time of adding to basket
    # This protects customers if the price changes while they're shopping
    price_at_addition = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Price of the artwork when added to basket"
    )
    
    # When this item was added to the basket
    added_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When this item was added to the basket"
    )
    
    class Meta:
        verbose_name = 'Basket Item'
        verbose_name_plural = 'Basket Items'
        # Ensure each artwork appears only once per basket
        unique_together = ['basket', 'artwork']
        ordering = ['-added_at']
    
    def __str__(self):
        """String representation of the basket item"""
        return f"{self.quantity}x {self.artwork.title} in {self.basket.user.username}'s basket"
    
    def get_subtotal(self):
        """
        Calculate the subtotal for this basket item.
        Subtotal = price × quantity
        
        Returns:
            Decimal: Total price for this item (price × quantity)
        """
        return self.price_at_addition * self.quantity
    
    def save(self, *args, **kwargs):
        """
        Override save method to automatically set price_at_addition
        if not already set.
        """
        # If price_at_addition is not set, use the current artwork price
        if not self.price_at_addition and self.artwork.price:
            self.price_at_addition = self.artwork.price
        
        super().save(*args, **kwargs)


# ============================================================================
# ORDER MODELS - Track completed purchases
# ============================================================================

class Order(models.Model):
    """
    Order model to track completed purchases.
    Created after successful payment processing.
    
    Features:
    - Links to user who made the purchase
    - Stores order details and status
    - Tracks payment information
    - Maintains order history
    """
    
    # Order status choices
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]
    
    # User who placed the order
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='orders',
        help_text="User who placed this order"
    )
    
    # Unique order number for reference
    order_number = models.CharField(
        max_length=32,
        unique=True,
        editable=False,
        help_text="Unique order reference number"
    )
    
    # Order status
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        help_text="Current status of the order"
    )
    
    # Total order amount
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Total order amount"
    )
    
    # Payment information
    payment_method = models.CharField(
        max_length=50,
        default='stripe',
        help_text="Payment method used (e.g., stripe, paypal)"
    )
    
    # Stripe payment intent ID for reference
    stripe_payment_intent = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Stripe payment intent ID"
    )
    
    # Customer contact information
    email = models.EmailField(
        help_text="Customer email address"
    )
    
    full_name = models.CharField(
        max_length=200,
        help_text="Customer full name"
    )
    
    # Billing address
    address_line1 = models.CharField(
        max_length=255,
        help_text="Address line 1"
    )
    
    address_line2 = models.CharField(
        max_length=255,
        blank=True,
        help_text="Address line 2 (optional)"
    )
    
    city = models.CharField(
        max_length=100,
        help_text="City"
    )
    
    postal_code = models.CharField(
        max_length=20,
        help_text="Postal/ZIP code"
    )
    
    country = models.CharField(
        max_length=100,
        help_text="Country"
    )
    
    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When the order was placed"
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="When the order was last updated"
    )
    
    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        ordering = ['-created_at']
    
    def __str__(self):
        """String representation of the order"""
        return f"Order {self.order_number} by {self.user.username if self.user else 'Guest'}"
    
    def save(self, *args, **kwargs):
        """
        Override save to generate unique order number if not set.
        """
        if not self.order_number:
            # Generate unique order number using timestamp and random string
            import uuid
            from datetime import datetime
            
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            unique_id = str(uuid.uuid4().hex[:8]).upper()
            self.order_number = f"ORD-{timestamp}-{unique_id}"
        
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    """
    Individual item within an order.
    Snapshot of purchased artwork at time of purchase.
    
    Features:
    - Links artwork to order
    - Stores artwork details at time of purchase
    - Maintains historical record even if artwork is deleted
    """
    
    # The order this item belongs to
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        help_text="The order containing this item"
    )
    
    # The artwork purchased (can be null if artwork is deleted later)
    artwork = models.ForeignKey(
        Artwork,
        on_delete=models.SET_NULL,
        null=True,
        related_name='order_items',
        help_text="The artwork purchased"
    )
    
    # Snapshot of artwork details at time of purchase
    artwork_title = models.CharField(
        max_length=200,
        help_text="Title of the artwork at time of purchase"
    )
    
    artwork_artist = models.CharField(
        max_length=200,
        help_text="Artist name at time of purchase"
    )
    
    artwork_medium = models.CharField(
        max_length=200,
        blank=True,
        help_text="Medium at time of purchase"
    )
    
    # Quantity purchased
    quantity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        help_text="Quantity purchased"
    )
    
    # Price at time of purchase
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Price at time of purchase"
    )
    
    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'
    
    def __str__(self):
        """String representation of the order item"""
        return f"{self.quantity}x {self.artwork_title} in order {self.order.order_number}"
    
    def get_subtotal(self):
        """
        Calculate subtotal for this order item.
        
        Returns:
            Decimal: Total price for this item
        """
        return self.price * self.quantity
