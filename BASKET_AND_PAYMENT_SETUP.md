# Shopping Basket & Payment Integration Setup Guide

## 🎉 What's Been Implemented

### 1. **Basket Functionality** ✅
- ✅ Basket models (Basket, BasketItem, Order, OrderItem)
- ✅ Add to basket functionality from artwork detail pages
- ✅ Update/remove items from basket
- ✅ Basket count display in navigation bar (with real-time updates)
- ✅ Clear basket functionality
- ✅ Basket page with comprehensive UI

### 2. **Checkout Flow** ✅
- ✅ Checkout page with billing address form
- ✅ Order summary sidebar
- ✅ Validation for empty baskets
- ✅ Progress indicator showing checkout steps

### 3. **Stripe Integration** ⏳ (Next Step)
- ✅ Stripe Python library installed
- ✅ Settings configured for Stripe API keys
- ⏳ Need to add Stripe API keys
- ⏳ Payment processing view
- ⏳ Stripe Elements integration
- ⏳ Order confirmation page

---

## 🔧 How to Complete the Setup

### Step 1: Get Your Stripe API Keys

1. **Create a Stripe Account** (if you don't have one)
   - Go to https://dashboard.stripe.com/register
   - Sign up for a free account

2. **Get Your Test API Keys**
   - Go to https://dashboard.stripe.com/test/apikeys
   - Copy your **Publishable key** (starts with `pk_test_`)
   - Copy your **Secret key** (starts with `sk_test_`)
   - **Important:** Keep your secret key private!

### Step 2: Add Stripe Keys to Environment

You have two options:

**Option A: Using Environment Variables (Recommended for Production)**
```powershell
# In PowerShell
$env:STRIPE_PUBLIC_KEY = "pk_test_YOUR_PUBLISHABLE_KEY_HERE"
$env:STRIPE_SECRET_KEY = "sk_test_YOUR_SECRET_KEY_HERE"
```

**Option B: Update settings.py Directly (For Development Only)**
Edit `config/settings.py` and replace the placeholder values:
```python
STRIPE_PUBLIC_KEY = 'pk_test_YOUR_ACTUAL_TEST_KEY_HERE'
STRIPE_SECRET_KEY = 'sk_test_YOUR_ACTUAL_SECRET_KEY_HERE'
```

---

## 📋 Testing the Basket Functionality

### 1. **Start the Development Server**
```powershell
python manage.py runserver
```

### 2. **Test the Basket Flow**

1. **Browse Artworks**
   - Go to http://localhost:8000/artworks/
   - Click on any artwork to view details

2. **Add to Basket**
   - Make sure you're logged in
   - Click "Add to Basket" button
   - You should see a success message
   - Notice the basket count in the navbar updates

3. **View Basket**
   - Click the basket icon in the navbar
   - You should see your items with:
     - Artwork image and details
     - Quantity controls (+ and -)
     - Remove button
     - Total price

4. **Update Quantities**
   - Use the +/- buttons to change quantities
   - The page will reload with updated totals

5. **Proceed to Checkout**
   - Click "Proceed to Checkout" button
   - Fill in the billing form
   - Review your order summary

---

## 🔐 Stripe Test Cards

When testing payments, use these test card numbers:

### Successful Payments
- **Card Number:** `4242 4242 4242 4242`
- **Expiry:** Any future date (e.g., 12/25)
- **CVC:** Any 3 digits (e.g., 123)
- **ZIP:** Any 5 digits (e.g., 12345)

### Declined Payment
- **Card Number:** `4000 0000 0000 0002`

### Requires Authentication (3D Secure)
- **Card Number:** `4000 0027 6000 3184`

---

## 🚀 Next Steps for Payment Processing

### 1. **Create Payment Processing View**
This will handle the actual payment with Stripe:

```python
# Add to collections_app/views.py

import stripe
from django.conf import settings

@login_required
@require_POST
def process_payment(request):
    """
    Process payment using Stripe API
    Creates a payment intent and charges the user's card
    """
    stripe.api_key = settings.STRIPE_SECRET_KEY
    
    # Get form data
    email = request.POST.get('email')
    # ... get other billing info ...
    
    # Get user's basket
    basket = Basket.objects.get(user=request.user)
    total_price = basket.get_total_price()
    
    try:
        # Create Stripe payment intent
        intent = stripe.PaymentIntent.create(
            amount=int(total_price * 100),  # Stripe uses cents
            currency='usd',
            description=f'Order from {request.user.email}',
            metadata={
                'user_id': request.user.id,
                'email': email,
            }
        )
        
        # Create Order record
        order = Order.objects.create(
            user=request.user,
            email=email,
            # ... add billing info ...
            total_price=total_price,
            status='completed',
            stripe_payment_intent_id=intent.id,
        )
        
        # Move basket items to order
        for item in basket.items.all():
            OrderItem.objects.create(
                order=order,
                artwork=item.artwork,
                quantity=item.quantity,
                price_at_purchase=item.price_at_addition,
            )
        
        # Clear basket
        basket.clear()
        
        messages.success(request, f'Payment successful! Order #{order.order_number}')
        return redirect('collections_app:order_success', order_id=order.id)
        
    except stripe.error.CardError as e:
        messages.error(request, f'Payment failed: {e.user_message}')
        return redirect('collections_app:checkout')
```

### 2. **Add Stripe Elements to Checkout Page**
Update `checkout.html` to include Stripe's payment form:

```html
<!-- Add before </body> -->
<script src="https://js.stripe.com/v3/"></script>
<script>
  // Initialize Stripe
  const stripe = Stripe('{{ STRIPE_PUBLIC_KEY }}');
  const elements = stripe.elements();
  
  // Create card element
  const card = elements.create('card');
  card.mount('#card-element');
  
  // Handle form submission
  const form = document.getElementById('checkout-form');
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const {paymentMethod, error} = await stripe.createPaymentMethod({
      type: 'card',
      card: card,
    });
    
    if (error) {
      // Display error
      document.getElementById('card-errors').textContent = error.message;
    } else {
      // Submit form with payment method ID
      const input = document.createElement('input');
      input.type = 'hidden';
      input.name = 'payment_method_id';
      input.value = paymentMethod.id;
      form.appendChild(input);
      form.submit();
    }
  });
</script>
```

### 3. **Create Order Success Page**
Create `templates/Vistor_pages/order_success.html`:

```html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-5 text-center">
  <i class="bi bi-check-circle-fill text-success" style="font-size: 5rem;"></i>
  <h1 class="mt-4">Order Confirmed!</h1>
  <p class="lead">Thank you for your purchase.</p>
  
  <div class="card mx-auto mt-4" style="max-width: 500px;">
    <div class="card-body">
      <h5>Order #{{ order.order_number }}</h5>
      <p class="text-muted">Confirmation email sent to {{ order.email }}</p>
      <hr>
      <p><strong>Total:</strong> ${{ order.total_price }}</p>
    </div>
  </div>
  
  <a href="{% url 'collections_app:artwork_list' %}" class="btn btn-primary mt-4">
    Continue Shopping
  </a>
</div>
{% endblock %}
```

---

## 📝 Database Schema

### Models Created

**Basket**
- `user`: One-to-one with User
- `created_at`, `updated_at`: Timestamps
- Methods: `get_total_price()`, `get_item_count()`, `clear()`

**BasketItem**
- `basket`: ForeignKey to Basket
- `artwork`: ForeignKey to Artwork
- `quantity`: Integer
- `price_at_addition`: Decimal (snapshot of artwork price)
- `added_at`: Timestamp
- Methods: `get_total_price()`

**Order**
- `user`: ForeignKey to User
- `order_number`: Unique identifier (auto-generated)
- `email`, `phone`: Contact info
- `address_line1`, `address_line2`, `city`, `state`, `postal_code`, `country`: Billing address
- `total_price`: Decimal
- `status`: choices (pending, completed, cancelled, refunded)
- `stripe_payment_intent_id`: Stripe reference
- `notes`: Optional customer notes
- `created_at`, `updated_at`: Timestamps

**OrderItem**
- `order`: ForeignKey to Order
- `artwork`: ForeignKey to Artwork
- `quantity`: Integer
- `price_at_purchase`: Decimal (snapshot of artwork price)
- `artist_name_at_purchase`: CharField (snapshot)
- `artwork_title_at_purchase`: CharField (snapshot)
- Methods: `get_total_price()`

---

## 🐛 Troubleshooting

### Issue: Basket count not updating
**Solution:** Make sure JavaScript is enabled and check browser console for errors.

### Issue: "Your basket is empty" on checkout
**Solution:** Add items to basket first. The checkout page requires at least one item.

### Issue: Stripe payment fails
**Solution:** 
1. Check that your Stripe API keys are correct
2. Use test card numbers from the list above
3. Check server logs for detailed error messages

### Issue: Static files not loading
**Solution:**
```powershell
python manage.py collectstatic
```

---

## 📚 Additional Resources

- **Stripe Documentation:** https://stripe.com/docs/payments
- **Django Documentation:** https://docs.djangoproject.com/
- **Stripe Testing:** https://stripe.com/docs/testing

---

## ✅ Checklist

- [x] Basket models created
- [x] Migrations applied
- [x] Basket views implemented
- [x] Basket templates created
- [x] Checkout page created
- [x] Stripe library installed
- [x] Settings configured
- [ ] Add Stripe API keys
- [ ] Test add to basket
- [ ] Test update/remove items
- [ ] Implement payment processing
- [ ] Create order success page
- [ ] Test full checkout flow
- [ ] Write unit tests

---

## 🎓 How It Works

1. **User browses artworks** → Clicks "Add to Basket"
2. **System creates/updates Basket** → Adds BasketItem with artwork reference
3. **Basket page displays items** → Shows quantities, prices, total
4. **User proceeds to checkout** → Fills billing form
5. **System processes payment** → Creates Stripe PaymentIntent
6. **Payment succeeds** → Creates Order with OrderItems
7. **Basket is cleared** → User receives confirmation
8. **Order is saved** → Admin can view in Django admin

---

**Status:** Ready for payment integration! Just add your Stripe API keys and test the flow. 🚀
