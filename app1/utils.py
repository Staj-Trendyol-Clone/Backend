from .models import Basket, ProductVariant

# If user have a basket get it, if not create one
def get_or_create_basket(user):
    basket, created = Basket.objects.get_or_create(user=user, is_active=True)
    return basket

# Does the stock supply demanded quantity   
def check_stock(variant, requested_quantity):
    if variant.var_stock < requested_quantity:
        raise Exception(f"Stok yetersiz! Bu üründen en fazla {variant.var_stock} adet alabilirsiniz.")
    return True

# Total price of the basket
def calculate_basket_total(basket):
    total = 0
    # Modellerde yazdığımız related_name='items' sayesinde sepetteki kalemlere ulaşıyoruz
    basket_items = basket.items.all() 
    
    for item in basket_items:
        # Varyantın fiyatı ile sepetteki adedi çarpıp toplama ekliyoruz
        if item.product_variant.var_price:
            total += (item.product_variant.var_price * item.quantity)
            
    return total