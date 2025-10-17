import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

from django.contrib.auth import get_user_model
from collections_app.models import (
    Art, ArtVariant, Basket, BasketItem, Order, OrderItem
)

User = get_user_model()

u = User.objects.filter(is_superuser=True).first()
if not u:
    print('No superuser found; aborting')
    raise SystemExit(1)

art = Art.objects.filter(variants__is_available=True).distinct().first()
if not art:
    print('No art with available variants found; aborting')
    raise SystemExit(1)

variant = ArtVariant.objects.filter(art=art, is_available=True).first()
if not variant:
    print('No available variant for art; aborting')
    raise SystemExit(1)

b, created = Basket.objects.get_or_create(user=u)
print('Basket id', b.pk, 'created?', created)

# ensure at least one BasketItem
if not b.items.exists():
    bi = BasketItem.objects.create(
        basket=b, art=art, variant=variant, quantity=1
    )
    print('Created BasketItem', bi.pk)
else:
    bi = b.items.first()
    print('Using existing BasketItem', bi.pk)

subtotal = b.get_total_price()
print('Basket subtotal', subtotal)

order = Order.objects.create(
    user=u,
    total_amount=subtotal,
    payment_method='admin-test',
    stripe_payment_intent='TEST',
    email=(u.email or ''),
    full_name=(u.get_full_name() or u.username),
    address_line1='Test Address',
    city='Nowhere',
    postal_code='00000',
    country='US',
)
print('Created Order', order.pk)

for bi in b.items.all():
    display = getattr(bi, 'display_artwork', None)
    variant_obj = getattr(bi, 'variant', None)
    oi = OrderItem.objects.create(
        order=order,
        art=(bi.art if getattr(bi, 'art', None) else None),
        artwork_title=(
            display.title if display else str(bi.price_at_addition)
        ),
        artwork_artist=(
            display.artist.name if getattr(display, 'artist', None) else ''
        ),
        artwork_medium=(
            display.medium if getattr(display, 'medium', None) else ''
        ),
        quantity=bi.quantity,
        price=bi.price_at_addition,
        variant_id=(variant_obj.pk if variant_obj else None),
        variant_medium=(
            variant_obj.get_medium_display() if variant_obj else ''
        ),
    )
    print(
        'Created OrderItem', oi.pk, 'variant_id=', oi.variant_id,
        'variant_medium=', oi.variant_medium,
    )

print('\nOrder items:')
for row in order.items.values(
    'id', 'artwork_title', 'price', 'variant_id', 'variant_medium'
):
    print(row)

# Clear basket for cleanliness
b.clear()
print('Cleared basket')
