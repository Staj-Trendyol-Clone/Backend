import graphene
from graphene_django import DjangoObjectType
from accounts.output import UserType
from decimal import Decimal
from .models import (
    Category, Product, Images, Comment, 
    Variation, VariationOption, ProductVariant, 
    Basket, BasketItem, Order, OrderItem, Favorite
)


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = "__all__"

class ProductType(DjangoObjectType):
    cover_image = graphene.String()

    product_total_quantity = graphene.Int()
    product_avr_price = graphene.Decimal(required=False)

    class Meta:
        model = Product
        fields = "__all__"

    def resolve_product_total_quantity(self, info):
        return self.product_total_quantity
    
    # Frontend'in çağırdığı productAvrPrice alanını ilk varyantın fiyatıyla doldurur
    def resolve_product_avr_price(self, info):
        first_variant = self.variants.first()
        if first_variant and first_variant.var_price is not None:
            return first_variant.var_price
        return Decimal('0.00')  # Float 0.0 yerine Decimal('0.00')
    
    # 2. Bu alanın içinin nasıl doldurulacağını hesaplayan fonksiyon
    def resolve_cover_image(self, info):
        # Ürüne ait ilk varyantı çekiyoruz
        ilk_varyant = self.variants.first()
        
        if ilk_varyant:
            # O varyanta ait ilk görseli çekiyoruz
            ilk_gorsel = ilk_varyant.images.first()
            
            if ilk_gorsel:
                # Görselin URL/dosya yolunu metin (string) olarak döndürüyoruz
                return str(ilk_gorsel.image)
                
        # Eğer ürüne henüz varyant veya görsel eklenmemişse boş dönüyoruz (sistem çökmesin diye)
        return None    

class ImagesType(DjangoObjectType):
    class Meta:
        model = Images
        fields = "__all__"


class CommentType(DjangoObjectType):
    user = graphene.Field(UserType, required=False)
    class Meta:
        model = Comment
        fields = "__all__"

class VariationType(DjangoObjectType):
    class Meta:
        model = Variation
        fields = "__all__"

class VariationOptionType(DjangoObjectType):
    class Meta:
        model = VariationOption
        fields = "__all__"

class ProductVariantType(DjangoObjectType):
    class Meta:
        model = ProductVariant
        fields = "__all__"

class BasketType(DjangoObjectType):
    class Meta:
        model = Basket
        fields = "__all__"

class BasketItemType(DjangoObjectType):
    class Meta:
        model = BasketItem
        fields = "__all__"

class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        fields = "__all__"

class OrderItemType(DjangoObjectType):
    class Meta:
        model = OrderItem
        fields = "__all__"        



class FavoriteType(DjangoObjectType):
    user = graphene.Field(UserType, required=False)

    class Meta:
        model = Favorite
        fields = "__all__"        