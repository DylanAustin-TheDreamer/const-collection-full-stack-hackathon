from django.db import models
from django.db.models import PROTECT
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
    # Legacy per-medium flags/prices (kept for Phase A compatibility).
    # These remain in the model temporarily so migrations and the DB
    # stay compatible during the phased rollout. They will be removed
    # by an explicit Phase-B migration when ready.
        # Note: legacy per-medium fields (physical_available/digital_available
        # and physical_price/digital_price) were removed in the Phase-B
        # migration; variants (ArtVariant) are now the source of truth.

    # --- ECOMMERCE / METADATA FIELDS (new, nullable) ---
    # unified price field (we'll map artwork.price to this by default)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )

    # Currency code for price display
    currency = models.CharField(max_length=3, default='USD', blank=True)

    # Availability flag for store
    is_available = models.BooleanField(default=False)

    # Featured flag for storefront
    is_featured = models.BooleanField(default=False)

    # Optional depth for 3D artworks
    depth_cm = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True
    )

    # Generic description field (from Artwork.description)
    description = models.TextField(blank=True)

    # Optional timestamps (nullable so existing rows are not affected)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    # (artwork_link removed after migration consolidation)

    def __str__(self):
        # Return a friendly string including artist for compatibility with
        # old Artwork
        artist = getattr(self.collection, 'artist', None)
        if artist:
            # ArtistProfile typically exposes name and email in tests
            artist_name = getattr(artist, 'name', str(artist))
            artist_email = getattr(artist, 'email', '')
            if artist_email:
                artist_email = f"<{artist_email}>"
            return f"{self.title} by {artist_name} {artist_email}".strip()
        return f"{self.title} ({self.collection.name})"

    @property
    def artist(self):
        """Compatibility property so templates expecting artwork.artist work on Art.
        Returns the ArtistProfile linked via the Art's collection."""
        return getattr(self.collection, 'artist', None)

    def get_size_display(self):
        """Return formatted size string similar to
        Artwork.get_size_display()."""
        if self.width_cm and self.height_cm:
            if getattr(self, 'depth_cm', None):
                return (
                    f"{self.width_cm} x {self.height_cm} x "
                    f"{self.depth_cm} cm"
                )
            return f"{self.width_cm} x {self.height_cm} cm"
        return "Size not specified"

    def get_price_display(self):
        """Return formatted price string similar to
        Artwork.get_price_display()."""
        if self.price:
            return f"{self.currency} {self.price:,.2f}"
        return "Price not available"

    def clean(self):
        # Phase B: validation is based on ArtVariant availability/pricing.
        # Keep a no-op here to preserve behavior for existing code paths.
        return


class ArtVariant(models.Model):
    ORIGINAL = 'original_piece'
    POSTER = 'printed_poster'
    DIGITAL = 'digital_copy'
    MEDIUM_CHOICES = [
        (ORIGINAL, 'Original piece'),
        (POSTER, 'Printed poster'),
        (DIGITAL, 'Digital copy'),
    ]

    art = models.ForeignKey(
        Art, on_delete=models.CASCADE, related_name='variants'
    )
    medium = models.CharField(max_length=32, choices=MEDIUM_CHOICES)
    is_available = models.BooleanField(default=False)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    currency = models.CharField(max_length=3, default='USD', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('art', 'medium')

    def __str__(self):
        return f"{self.get_medium_display()} — {self.art.title}"

# ============================================================================
# BASKET MODELS - Shopping cart functionality for purchasing artworks
# =============================================================================

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
    
    # The canonical art reference (only 'art' now remains)
    art = models.ForeignKey(
        'Art',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='basket_items',
        help_text="The linked Art for this basket item",
    )

    # Optional specific variant (format) selected by the user
    variant = models.ForeignKey(
        'ArtVariant',
        null=False,
        blank=False,
        on_delete=PROTECT,
        related_name='basket_items',
        help_text="Selected ArtVariant (format)",
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
        # Allow multiple items per art if different variants are chosen
        unique_together = ['basket', 'art', 'variant']
        ordering = ['-added_at']
    
    def __str__(self):
        """String representation of the basket item"""
        display = self.display_artwork
        title = display.title if display else 'Unknown artwork'
        return (
            f"{self.quantity}x {title} in "
            f"{self.basket.user.username}'s basket"
        )
    
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
        # Variant is required in Phase B; ensure it's present
        if not getattr(self, 'variant', None):
            raise ValueError('BasketItem.variant is required')

        # Snapshot the variant price at time of add
        if not self.price_at_addition:
            if getattr(self.variant, 'price', None) is not None:
                self.price_at_addition = self.variant.price
            else:
                # Fallback to Art.price if variant price missing
                self.price_at_addition = getattr(self.art, 'price', None) or 0

        super().save(*args, **kwargs)

    @property
    def display_artwork(self):
        """Return the canonical Art instance for display purposes."""
        return getattr(self, 'art', None)


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
        return (
            f"Order {self.order_number} by "
            f"{self.user.username if self.user else 'Guest'}"
        )
    
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
    
    # The art purchased (snapshot stored separately). Keep art FK for history.
    art = models.ForeignKey(
        'Art', null=True, blank=True, on_delete=models.SET_NULL,
        related_name='order_items', help_text="The Art purchased"
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
    # Snapshot of the selected variant at time of purchase (if any)
    variant_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="ArtVariant primary key at time of purchase (nullable)"
    )

    variant_medium = models.CharField(
        max_length=50,
        blank=True,
        help_text=(
            "Human-readable medium/format of the variant at time of purchase"
        )
    )
    
    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'
    
    def __str__(self):
        """String representation of the order item"""
        return (
            f"{self.quantity}x {self.artwork_title} in order "
            f"{self.order.order_number}"
        )
    
    def get_subtotal(self):
        """
        Calculate subtotal for this order item.
        
        Returns:
            Decimal: Total price for this item
        """
        return self.price * self.quantity
