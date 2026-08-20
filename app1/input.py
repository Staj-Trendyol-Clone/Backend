import graphene

# 1. Adding a product variation to the basket, required inputs:
class AddToBasketInput(graphene.InputObjectType):
    # Variant id as an input
    product_variant_id = graphene.ID(required=True)
    quantity = graphene.Int(default_value=1)

# 2. Updating quantitiy of a basket item, required inputs:
class UpdateBasketItemInput(graphene.InputObjectType):
    basket_item_id = graphene.ID(required=True)
    quantity = graphene.Int(required=True)

# 3. Deleting a basket item from the basket, required inputs:
class RemoveFromBasketInput(graphene.InputObjectType):
    basket_item_id = graphene.ID(required=True)

# 4. Filter products according to their category, all inputs are optional:
class ProductFilterInput(graphene.InputObjectType):
    category_id = graphene.ID(required=False)
    category_name = graphene.String(required=False)
    search = graphene.String(required=False)   

class CommentInput(graphene.InputObjectType):
    product_id = graphene.ID(required=True)
    stars = graphene.Int(required=True)
    comment = graphene.String(required=True)     


class ToggleFavoriteInput(graphene.InputObjectType):
    product_id = graphene.ID(required=True)
