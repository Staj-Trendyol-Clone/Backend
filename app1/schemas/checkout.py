import graphene
from django.db import transaction
from app1.models import BasketItem, Order, OrderItem
from app1.output import OrderType
from app1.utils import get_or_create_basket, calculate_basket_total

class CheckoutBasket(graphene.Mutation):
    message = graphene.String()
    order = graphene.Field(OrderType)

    # Dışarıdan ID beklemiyoruz, çünkü kullanıcının kendi sepetini çekeceğiz.
    def mutate(self, info):
        user = info.context.user

        if user.is_anonymous:
            raise Exception("Sipariş vermek için lütfen giriş yapın.")

        basket = get_or_create_basket(user)
        basket_items = BasketItem.objects.filter(basket=basket)

        if not basket_items.exists():
            raise Exception("Sepetiniz boş. Sipariş oluşturulamadı.")

        total_amount = calculate_basket_total(basket)

        # Hata durumunda veritabanını korumak için transaction kullanıyoruz
        with transaction.atomic():
            
            user_shipping_address = getattr(user, 'address', None) or "Adres belirtilmedi"

            # 1. YENİ BİR SİPARİŞ (ORDER) OLUŞTUR
            order = Order.objects.create(
                user=user,
                total_amount=total_amount,
                shipping_address=user_shipping_address
            )

            # 2. SEPETTEKİ ÜRÜNLERİ DÖNGÜYE AL VE SİPARİŞ KALEMİNE (ORDER ITEM) ÇEVİR
            for item in basket_items:
                OrderItem.objects.create(
                    order=order,
                    product_variant=item.product_variant,
                    quantity=item.quantity,
                    price_at_time_of_purchase=item.product_variant.var_price
                )
                
                # Ürün satın alındığı için stoktan düşebilirsin
                variant = item.product_variant
                if variant.var_stock >= item.quantity:
                    variant.var_stock -= item.quantity
                    variant.save()

            # 3. SEPETİN İÇİNİ TAMAMEN TEMİZLE
            basket_items.delete()

        return CheckoutBasket(
            message="Siparişiniz başarıyla alındı ve sepetiniz temizlendi.",
            order=order
        )
