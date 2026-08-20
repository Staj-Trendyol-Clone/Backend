from django.contrib import admin
from .models import (
    Product, Images, Order, OrderItem, Category, 
    Comment, Variation, ProductVariant, VariationOption, 
    Basket, BasketItem, Favorite
)

# ----------------- INLINES (İç İçe Tablolar) -----------------

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product_variant', 'quantity', 'price_at_time_of_purchase')

class BasketItemInline(admin.TabularInline):
    model = BasketItem
    extra = 0

# ----------------- ADMIN GÖRÜNÜMLERİ -----------------

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_name', 'get_first_variant_price', 'product_total_quantity', 'product_is_active', 'created_at')
    search_fields = ('product_name',)
    readonly_fields = ('get_first_variant_price',)


    @admin.display(description="İlk Varyant Fiyatı (Vitrin Fiyatı)")
    def get_first_variant_price(self, obj):
        first_variant = obj.variants.first()
        if first_variant and first_variant.var_price is not None:
            return f"{first_variant.var_price} TL"
        return "Varyant Yok (0.00 TL)"
   

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'stars', 'created_at')
    list_filter = ('stars', 'created_at')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_amount', 'status', 'created_at')
    inlines = [OrderItemInline]

@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
    inlines = [BasketItemInline]

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'var_price', 'var_stock')

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'product__product_name')
    readonly_fields = ('created_at',)    

# ----------------- DİĞER STANDART MODELLER -----------------

admin.site.register(Category)
admin.site.register(Images)
admin.site.register(Variation)
admin.site.register(VariationOption)