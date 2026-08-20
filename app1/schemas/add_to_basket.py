import graphene
from app1.models import ProductVariant, BasketItem
from app1.output import BasketType
from app1.input import AddToBasketInput
from app1.utils import get_or_create_basket, check_stock, calculate_basket_total

class AddToBasket(graphene.Mutation):
    # 1. Frontend'den Hangi Formu Bekliyoruz? (Input)
    class Arguments:
        data = AddToBasketInput(required=True)

    # 2. İşlem Bitince Frontend'e Ne Döndüreceğiz? (Output)
    basket = graphene.Field(BasketType)
    message = graphene.String()
    total_price = graphene.Float()

    # 3. Asıl İşlemin Yapıldığı Yer (Mutate)
    def mutate(self, info, data):
        user = info.context.user

        if user.is_anonymous:
            raise Exception("Sepetinize ürün eklemek için lütfen giriş yapın.")

        variant_id = data.product_variant_id
        quantity = data.quantity

        # B. Varyant veritabanında var mı?
        try:
            variant = ProductVariant.objects.get(id=variant_id)
        except ProductVariant.DoesNotExist:
            raise Exception("Böyle bir ürün varyantı bulunamadı.")

        # C. KORUMA 1: Stok var mı? (Utils fonksiyonumuz çalışıyor)
        check_stock(variant, quantity)

        # D. KORUMA 2: Kullanıcının sepetini getir (Utils fonksiyonumuz çalışıyor)
        basket = get_or_create_basket(user)

        # E. Sepette bu üründen zaten var mı kontrolü (unique_together mantığı)
        basket_item = BasketItem.objects.filter(basket=basket, product_variant=variant).first()
        
        if basket_item:
            # Sepette zaten varsa, adedi artırıyoruz
            yeni_adet = basket_item.quantity + quantity
            # Yeni toplam adet için stok kontrolünü tekrar yapıyoruz
            check_stock(variant, yeni_adet)
            
            basket_item.quantity = yeni_adet
            basket_item.save()
            message = "Sepetinizdeki ürün adedi güncellendi."
        else:
            # Sepette yoksa yepyeni bir satır olarak ekliyoruz
            BasketItem.objects.create(
                basket=basket,
                product_variant=variant,
                quantity=quantity
            )
            message = "Ürün sepetinize başarıyla eklendi."

        # F. KORUMA 3: Sepetin yeni toplam tutarını hesapla (Utils fonksiyonumuz çalışıyor)
        total_price = calculate_basket_total(basket)

        # G. Sonuçları frontend'e gönder
        return AddToBasket(
            basket=basket, 
            message=message, 
            total_price=total_price
        )

