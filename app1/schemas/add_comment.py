import graphene
from app1.models import Product, Comment, OrderItem
from app1.output import CommentType
from app1.input import CommentInput


class AddComment(graphene.Mutation):
    class Arguments:
        data = CommentInput(required=True)

    message = graphene.String()
    comment = graphene.Field(CommentType)

    def mutate(self, info, data):
        user = info.context.user

        # 1. Oturum Kontrolü
        if user.is_anonymous:
            raise Exception("Yorum yapabilmek için lütfen giriş yapın.")

        # 2. Puan Sınırı Kontrolü (1 - 5 arası)
        if not (1 <= data.stars <= 5):
            raise Exception("Yıldız puanı 1 ile 5 arasında olmalıdır.")

        # 3. Ürün Kontrolü
        try:
            product = Product.objects.get(id=data.product_id)
        except Product.DoesNotExist:
            raise Exception("Değerlendirilmek istenen ürün bulunamadı.")

        # 4. Satın Alma Kontrolü
        has_purchased = OrderItem.objects.filter(
            order__user=user,
            product_variant__product=product
        ).exists()

        if not has_purchased:
            raise Exception("Yalnızca satın aldığınız ürünlere yorum ve puan bırakabilirsiniz.")
        
        # 5. Aynı yorumdan var mı?
        if Comment.objects.filter(user=user, product=product).exists():
          raise Exception("Bu ürün için zaten bir değerlendirmeniz bulunmaktadır.")

        # 6. Yorumu Kaydetme
        new_comment = Comment.objects.create(
            user=user,
            product=product,
            stars=data.stars,
            comment=data.comment
        )

        return AddComment(
            message="Yorumunuz ve puanınız başarıyla kaydedildi.",
            comment=new_comment
        )