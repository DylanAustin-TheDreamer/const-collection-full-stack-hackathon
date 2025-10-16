from django.contrib import admin
from django.utils.html import format_html
from .models import Collection, Art, Artwork, Basket, BasketItem, Order, OrderItem


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):

    list_display = ('name', 'artist', 'cover_preview')
    search_fields = ('name', 'artist__name')
    list_filter = ('artist',)
    list_display_links = ('name',)
    inlines = []

    def cover_preview(self, obj):
        if obj.cover_image:
            return format_html(
                '<img src="{}" style="max-height:75px;" />',
                obj.cover_image.url,
            )
        return ''

    cover_preview.short_description = 'Cover'


@admin.register(Art)
class ArtAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'collection',
        'year_created',
        'physical_available',
        'physical_price',
        'digital_available',
        'digital_price',
        'image_preview',
    )
    search_fields = ('title', 'collection__name')
    list_filter = ('collection',)

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height:75px;" />',
                obj.image.url,
            )
        return ''

    image_preview.short_description = 'Image'


# Inline so admins can add Art from a Collection page
class ArtInline(admin.TabularInline):
    model = Art
    extra = 1
    fields = ('title', 'image', 'physical_available', 'physical_price')


# Attach the inline to the CollectionAdmin dynamically to avoid
# import order issues
CollectionAdmin.inlines = [ArtInline]


# ============================================================================
# ARTWORK ADMIN - Admin interface for the new Artwork model
# ============================================================================

@admin.register(Artwork)
class ArtworkAdmin(admin.ModelAdmin):
    """
    Admin interface for Artwork model.
    Provides comprehensive management of artworks with price, size, and medium.
    """
    
    list_display = (
        'title',
        'artist',
        'medium',
        'price',
        'currency',
        'size_display',
        'is_available',
        'is_featured',
        'created_at',
        'artwork_image_preview',
    )
    
    list_filter = (
        'is_available',
        'is_featured',
        'currency',
        'artist',
        'created_at',
    )
    
    search_fields = (
        'title',
        'artist__name',
        'medium',
        'description',
    )
    
    list_editable = (
        'is_available',
        'is_featured',
        'price',
    )
    
    readonly_fields = (
        'created_at',
        'updated_at',
        'artwork_image_preview',
    )
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'artist', 'description', 'image', 'artwork_image_preview')
        }),
        ('Artwork Details', {
            'fields': ('medium', 'year_created', 'width_cm', 'height_cm', 'depth_cm')
        }),
        ('Pricing', {
            'fields': ('price', 'currency', 'is_available')
        }),
        ('Display Options', {
            'fields': ('is_featured',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def artwork_image_preview(self, obj):
        """Display artwork image preview in admin"""
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height:200px; max-width:200px;" />',
                obj.image.url,
            )
        return 'No image'
    
    artwork_image_preview.short_description = 'Image Preview'
    
    def size_display(self, obj):
        """Display formatted size in list view"""
        return obj.get_size_display()
    
    size_display.short_description = 'Size'


# ============================================================================
# BASKET ADMIN - Admin interface for shopping baskets
# ============================================================================

class BasketItemInline(admin.TabularInline):
    """
    Inline admin for basket items.
    Allows viewing/editing basket items directly from the basket admin.
    """
    model = BasketItem
    extra = 0
    readonly_fields = ('added_at', 'get_subtotal_display')
    fields = ('artwork', 'quantity', 'price_at_addition', 'added_at', 'get_subtotal_display')
    
    def get_subtotal_display(self, obj):
        """Display subtotal for each basket item"""
        if obj.pk:
            return f"${obj.get_subtotal():,.2f}"
        return "-"
    
    get_subtotal_display.short_description = 'Subtotal'


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    """
    Admin interface for Basket model.
    Manage user shopping baskets.
    """
    
    list_display = (
        'user',
        'get_item_count_display',
        'get_total_display',
        'updated_at',
        'created_at',
    )
    
    list_filter = ('created_at', 'updated_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at', 'get_total_display', 'get_item_count_display')
    
    inlines = [BasketItemInline]
    
    def get_item_count_display(self, obj):
        """Display number of items in basket"""
        return obj.get_item_count()
    
    get_item_count_display.short_description = 'Items'
    
    def get_total_display(self, obj):
        """Display total basket value"""
        return f"${obj.get_total_price():,.2f}"
    
    get_total_display.short_description = 'Total'


@admin.register(BasketItem)
class BasketItemAdmin(admin.ModelAdmin):
    """
    Admin interface for BasketItem model.
    Manage individual basket items.
    """
    
    list_display = (
        'basket',
        'artwork',
        'quantity',
        'price_at_addition',
        'get_subtotal_display',
        'added_at',
    )
    
    list_filter = ('added_at',)
    search_fields = ('basket__user__username', 'artwork__title')
    readonly_fields = ('added_at', 'get_subtotal_display')
    
    def get_subtotal_display(self, obj):
        """Display subtotal for basket item"""
        return f"${obj.get_subtotal():,.2f}"
    
    get_subtotal_display.short_description = 'Subtotal'


# ============================================================================
# ORDER ADMIN - Admin interface for completed orders
# ============================================================================

class OrderItemInline(admin.TabularInline):
    """
    Inline admin for order items.
    Allows viewing order items directly from the order admin.
    """
    model = OrderItem
    extra = 0
    readonly_fields = ('artwork', 'artwork_title', 'artwork_artist', 'artwork_medium', 'quantity', 'price', 'get_subtotal_display')
    fields = ('artwork', 'artwork_title', 'artwork_artist', 'quantity', 'price', 'get_subtotal_display')
    
    def get_subtotal_display(self, obj):
        """Display subtotal for each order item"""
        if obj.pk:
            return f"${obj.get_subtotal():,.2f}"
        return "-"
    
    get_subtotal_display.short_description = 'Subtotal'
    
    def has_add_permission(self, request, obj=None):
        """Prevent adding items to completed orders"""
        return False
    
    def has_delete_permission(self, request, obj=None):
        """Prevent deleting items from completed orders"""
        return False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Admin interface for Order model.
    Manage completed purchases and order history.
    """
    
    list_display = (
        'order_number',
        'user',
        'full_name',
        'email',
        'status',
        'total_amount',
        'payment_method',
        'created_at',
    )
    
    list_filter = (
        'status',
        'payment_method',
        'created_at',
    )
    
    search_fields = (
        'order_number',
        'user__username',
        'email',
        'full_name',
        'stripe_payment_intent',
    )
    
    list_editable = ('status',)
    
    readonly_fields = (
        'order_number',
        'stripe_payment_intent',
        'created_at',
        'updated_at',
        'total_amount',
    )
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'user', 'status', 'total_amount')
        }),
        ('Customer Information', {
            'fields': ('full_name', 'email')
        }),
        ('Billing Address', {
            'fields': ('address_line1', 'address_line2', 'city', 'postal_code', 'country')
        }),
        ('Payment Details', {
            'fields': ('payment_method', 'stripe_payment_intent')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [OrderItemInline]
    
    def has_delete_permission(self, request, obj=None):
        """
        Prevent deletion of orders for record-keeping.
        Orders should be marked as cancelled instead.
        """
        return False


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """
    Admin interface for OrderItem model.
    View individual order items.
    """
    
    list_display = (
        'order',
        'artwork_title',
        'artwork_artist',
        'artwork_medium',
        'quantity',
        'price',
        'get_subtotal_display',
    )
    
    list_filter = ('order__created_at',)
    search_fields = ('order__order_number', 'artwork_title', 'artwork_artist')
    readonly_fields = ('order', 'artwork', 'artwork_title', 'artwork_artist', 'artwork_medium', 'quantity', 'price')
    
    def get_subtotal_display(self, obj):
        """Display subtotal for order item"""
        return f"${obj.get_subtotal():,.2f}"
    
    get_subtotal_display.short_description = 'Subtotal'
    
    def has_add_permission(self, request):
        """Prevent manual addition of order items"""
        return False
    
    def has_delete_permission(self, request, obj=None):
        """Prevent deletion of order items for record-keeping"""
        return False
