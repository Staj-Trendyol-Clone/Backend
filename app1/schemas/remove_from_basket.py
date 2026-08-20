import graphene
from app1.models import BasketItem
from app1.output import BasketType
from app1.input import RemoveFromBasketInput
from app1.utils import get_or_create_basket, calculate_basket_total

class RemoveFromBasket(graphene.Mutation):
    
    class Arguments:
        data = RemoveFromBasketInput(required=True)

    basket = graphene.Field(BasketType)
    message = graphene.String()
    total_price = graphene.Float()

    def mutate(self, info, data):
        user = info.context.user
        
        if user.is_anonymous:
          raise Exception("Bu işlem için lütfen giriş yapın.")

        basket_item_id = data.basket_item_id
        
        # İşlemi yapan kullanıcının kendi sepetini getiriyoruz
        basket = get_or_create_basket(user)

        try:
            # GÜVENLİK DUVARI: Hem ID'si eşleşen hem de BU SEPATA ait olan satırı bul
            basket_item = BasketItem.objects.get(id=basket_item_id, basket=basket)
            
            # Satırı bulduysak direkt veritabanından siliyoruz
            basket_item.delete()
            message = "Ürün sepetinizden başarıyla silindi."
            
        except BasketItem.DoesNotExist:
            # Eğer o ID'de bir satır yoksa veya var ama BAŞKA BİRİNİN sepetindeyse bu hata döner
            raise Exception("Bu ürün sepetinizde bulunmuyor veya zaten silinmiş.")

        # Ürün silindiği için toplam fiyatı yeniden hesaplatıyoruz
        total_price = calculate_basket_total(basket)

        return RemoveFromBasket(
            basket=basket, 
            message=message, 
            total_price=total_price
        )
