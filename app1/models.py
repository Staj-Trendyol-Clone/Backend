from django.db import models
from django.core.validators import (
MinValueValidator, MaxValueValidator,)
from django.conf import settings 
from django.core.exceptions import ValidationError
from django.db.models import Sum


### Category Model ###
class Category(models.Model):
  category_name= models.CharField(max_length=50)
  category_is_active = models.BooleanField(default=True)

  def __str__(self):
    return self.category_name

### Product Model ###
class Product(models.Model):
    product_name = models.CharField(max_length=50)
    product_description = models.TextField()
    product_avr_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.00)
    product_is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    @property
    def product_total_quantity(self):
        # Total stock of all variants of a product
        total = self.variants.aggregate(total=Sum('var_stock'))['total']
        return total or 0

    #Many-to-many between category and product model
    categories = models.ManyToManyField(Category,related_name='products')

    class Meta:
        ordering = ['-created_at'] 
    def __str__(self):
        return self.product_name
    
### Images Model ###
class Images(models.Model):
  # One-to-many relation between product and images
  product = models.ForeignKey('ProductVariant', on_delete=models.CASCADE, related_name='images')
  image = models.ImageField(upload_to='product_images/')
  created_at = models.DateTimeField(auto_now_add=True)

  class Meta:
    verbose_name = 'Ürün Görseli'          
    verbose_name_plural = 'Ürün Görselleri'
    ordering = ['-created_at'] # ordering, starting from latest one

  def __str__(self):
        return f"{self.product.product} - Görsel {self.id}"  


### Comment Model ###
class Comment(models.Model):
  user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='comments',
        blank=True
    )
  product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comment')
  # Star constraint between 1-5
  stars = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
  comment = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True) 

  class Meta:
    unique_together = ('user', 'product')
    verbose_name = 'Yorum'
    verbose_name_plural = 'Yorumlar'
    ordering = ['-created_at'] 

  def __str__(self):
        username = self.user.username if self.user else "Anonim"
        return f"{username} - {self.product.product_name} ({self.stars} Yıldız)"
    

### Variation Model ###
class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variations')
    var_name = models.CharField(max_length=100) 

    class Meta:
        verbose_name = 'Varyasyon'
        verbose_name_plural = 'Varyasyonlar'
        # constraint for not adding the same variant combinations to a product
        constraints = [
            models.UniqueConstraint(fields=['product', 'var_name'], name='unique_product_variation')
        ]

    def __str__(self):
        return f"{self.product.product_name} - {self.var_name}"    


### VariationOption Model ###
class VariationOption(models.Model):
    variation = models.ForeignKey(Variation, on_delete=models.CASCADE, related_name='options')
    var_option_value = models.CharField(max_length=100) # Örn: "42", "Siyah"

    class Meta:
        verbose_name = 'Varyasyon Seçeneği'
        verbose_name_plural = 'Varyasyon Seçenekleri'

    def __str__(self):
        return f"{self.variation.var_name}: {self.var_option_value}"

### ProductVariant Model ###
class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')

    #a product can have many variant options
    options = models.ManyToManyField(VariationOption, related_name='variant_items')    
    var_stock = models.PositiveIntegerField(default=0)
    var_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        verbose_name = 'Stok & Varyant'
        verbose_name_plural = 'Stoklar & Varyantlar'

    def __str__(self):
        return f"{self.product.product_name} - Varyant {self.id}"
    
### Basket Model ###
class Basket(models.Model):
    # Importing user model from settings
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name="basket"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - Sepeti"    
    
### Basket Item Model ###    
class BasketItem(models.Model):
    # related basket:
    basket = models.ForeignKey(
        'Basket', 
        on_delete=models.CASCADE, 
        related_name='items'
    )
    
    # which variant of a product will be added:
    product_variant = models.ForeignKey(
        'ProductVariant', 
        on_delete=models.CASCADE,
        related_name='basket_items'
    )
    
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
    # It prevents having two separate lines of the same variant in the same basket.
      unique_together = ('basket', 'product_variant')

    # Stock Control
    def clean(self):
        super().clean() # Django'nun standart doğrulamalarını çalıştır
        
        # 1. Varyant seçilmiş mi kontrolü (Boşken hata vermemesi için)
        if self.product_variant:
            
            # 2. Stok Kontrolü 
            if self.quantity > self.product_variant.var_stock:
                raise ValidationError({
                    'quantity': f"Stok hatası! Bu üründen stokta sadece {self.product_variant.var_stock} adet var."
                })
            
            # 3. Sıfır veya Eksi Değer Kontrolü (Güvenlik için)
            if self.quantity <= 0:
                raise ValidationError({
                    'quantity': "Ürün adedi en az 1 olmalıdır."
                })

    def __str__(self):
        return f"{self.quantity} x {self.product_variant}"
    
### Order Model ###   
class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="orders"
    )
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_address = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=50, default="Tamamlandı")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Sipariş'
        verbose_name_plural = 'Siparişler'
        ordering = ['-created_at']

    def __str__(self):
        return f"Sipariş {self.id} - {self.user.username}"

### Order Item Model ###   
class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, 
        on_delete=models.CASCADE, 
        related_name="items"
    )
    product_variant = models.ForeignKey(
        'ProductVariant', 
        on_delete=models.SET_NULL,
        null=True
    )
    quantity = models.PositiveIntegerField()
    price_at_time_of_purchase = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} adet (Sipariş: {self.order.id})"    


class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorites')
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Aynı kullanıcının aynı ürünü birden fazla kez favorilemesini engeller
        unique_together = ('user', 'product')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.product.product_name}"


