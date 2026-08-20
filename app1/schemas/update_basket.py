import graphene
from django.core.exceptions import ValidationError
from app1.models import BasketItem
from app1.output import BasketType
from app1.utils import get_or_create_basket

class UpdateBasketInput(graphene.InputObjectType):
    # Hangi sepet satırını güncelleyeceğimizi bilmek için ID:
    basket_item_id = graphene.ID(required=True)
    # Yeni miktar kaç olacak?
    quantity = graphene.Int(required=True)

class UpdateBasket(graphene.Mutation):
    class Arguments:
        data = UpdateBasketInput(required=True)

    message = graphene.String()
    basket = graphene.Field(BasketType)
    # Eğer toplam fiyat dönüyorsan buraya total_price = graphene.Float() ekleyebilirsin

    @classmethod
    def mutate(cls, root, info, data):
        # 1. KULLANICI GÜVENLİK DUVARI
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Sepetinizi güncellemek için lütfen giriş yapın.")

        basket = get_or_create_basket(user)

        try:
            # 2. ÜRÜNÜ BUL (Sadece bu müşterinin sepetinde olan bir ürünü arıyoruz)
            basket_item = BasketItem.objects.get(id=data.basket_item_id, basket=basket)
            
            # 3. YENİ MİKTARI KONTROL ET
            new_quantity = data.quantity
            
            # Müşteri 0 gönderdiyse bunu silme işlemi say veya hata ver:
            if new_quantity <= 0:
                raise Exception("Ürün adedi en az 1 olmalıdır. Silmek istiyorsanız sil butonunu kullanın.")
            
            # 4. GÜNCELLE VE KAYDET
            basket_item.quantity = new_quantity
            
            # DİKKAT: models.py içine yazdığımız stok kontrolünün (clean metodunun) 
            # çalışması için kaydetmeden önce full_clean() çağırıyoruz!
            basket_item.full_clean() 
            basket_item.save()

            return UpdateBasket(
                message="Sepetiniz başarıyla güncellendi.",
                basket=basket
            )

        except BasketItem.DoesNotExist:
            raise Exception("Bu ürün sepetinizde bulunamadı.")
        except ValidationError as e:
            # Stok yetersizse models.py'dan gelen hatayı frontend'e fırlatıyoruz
            # e.messages listesindeki ilk hatayı alıyoruz
            raise Exception(e.messages[0])