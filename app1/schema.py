import graphene

# app1 içindeki tüm sorgu ve mutasyonları SADECE buraya import ediyoruz
from app1.schemas.queries import Query as App1Query
from app1.schemas.add_to_basket import AddToBasket 
from app1.schemas.remove_from_basket import RemoveFromBasket 
from app1.schemas.update_basket import UpdateBasket 
from app1.schemas.checkout import CheckoutBasket
from app1.schemas.add_comment import AddComment
from app1.schemas.favorites import ToggleFavorite

# Queries of app1 
class Query(App1Query, graphene.ObjectType):
    pass

# Mutations of app1
class Mutation(graphene.ObjectType):
    add_to_basket = AddToBasket.Field()
    remove_from_basket = RemoveFromBasket.Field()
    update_basket = UpdateBasket.Field()
    checkout_basket = CheckoutBasket.Field()
    add_comment = AddComment.Field()
    toggle_favorite = ToggleFavorite.Field()