import graphene
from app1.models import Favorite, Product
from app1.output import FavoriteType
from app1.input import ToggleFavoriteInput  # Input'u import ediyoruz

class ToggleFavorite(graphene.Mutation):
    class Arguments:
        data = ToggleFavoriteInput(required=True)

    message = graphene.String()
    is_favorited = graphene.Boolean()
    favorite = graphene.Field(FavoriteType, required=False)

    def mutate(self, info, data):
        user = info.context.user

        if user.is_anonymous:
            raise Exception("Favorilere eklemek için giriş yapmalısınız.")

        try:
            product = Product.objects.get(id=data.product_id)
        except Product.DoesNotExist:
            raise Exception("Ürün bulunamadı.")

        favorite = Favorite.objects.filter(user=user, product=product).first()

        if favorite:
            favorite.delete()
            return ToggleFavorite(
                message="Ürün favorilerden kaldırıldı.",
                is_favorited=False,
                favorite=None
            )
        else:
            new_fav = Favorite.objects.create(user=user, product=product)
            return ToggleFavorite(
                message="Ürün favorilere eklendi.",
                is_favorited=True,
                favorite=new_fav
            )