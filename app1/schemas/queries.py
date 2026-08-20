import graphene
from app1.output import ProductType, BasketType, CategoryType, OrderType, FavoriteType
from app1.models import Product, Category, Order, Favorite
from app1.input import ProductFilterInput
from app1.utils import get_or_create_basket
from django.db.models import Q


class Query(graphene.ObjectType):
    # Field def. for frontend
    all_products = graphene.List(
        ProductType,
        filter=ProductFilterInput(required=False)
        )
    all_categories = graphene.List(CategoryType)
    product_detail = graphene.Field(ProductType, id=graphene.ID(required=True))
    my_basket = graphene.Field(BasketType)
    my_favorites = graphene.List(FavoriteType)

    #for autocomplete 
    category_suggestions = graphene.List(
        CategoryType, 
        search_text=graphene.String(required=True)
    )

    my_orders = graphene.List(OrderType)


    # Category suggestions while searching for a category
    def resolve_category_suggestions(self, info, search_text):
        # Eğer arama metni 2 karakterden kısaysa boş liste dön (performans için)
        if len(search_text) < 2:
            return Category.objects.none()
            
        # İçinde aranan kelime geçen aktif kategorileri bul
        return Category.objects.filter(
            category_is_active=True,
            category_name__icontains=search_text
        )[:5] # Sadece en alakalı ilk 5 kategoriyi öner (Arayüz kalabalık olmasın)
    
    # Resolver for orders
    def resolve_my_orders(self, info):
        user = info.context.user
        
        if user.is_anonymous:
            raise Exception("Geçmiş siparişlerinizi görmek için lütfen giriş yapın.")
            
        # Sadece isteği atan kullanıcıya ait siparişleri getir
        # (Modellerde '-created_at' yaptığımız için zaten en yeniler en üstte gelecek)
        return Order.objects.filter(user=user)
    
    # Resolver for categories
    def resolve_all_categories(self, info):
        return Category.objects.filter(category_is_active=True)
    
    # Resolver for all products and filtering
    def resolve_all_products(self, info, filter=None):
        # 1. Başlangıç QuerySet'i
        qs = Product.objects.filter(product_is_active=True)

        # 2. Filtre Kontrolleri
        if filter:
            if filter.category_id:
                qs = qs.filter(categories__id=filter.category_id)
            
            if filter.category_name:
                qs = qs.filter(categories__category_name__icontains=filter.category_name)
            
            if filter.search:
                qs = qs.filter(
                    Q(product_name__icontains=filter.search) |
                    Q(product_description__icontains=filter.search)
                )

        return qs.distinct()
    
    # Resolver for product detail
    def resolve_product_detail(self, info, id):
        try:
            # IDs match and product is active
            return Product.objects.get(id=id, product_is_active=True)
        except Product.DoesNotExist:
            # If not raise exception
            raise Exception("Aradığınız ürün bulunamadı veya artık satışta değil.")
    
    # Resolver for basket
    def resolve_my_basket(self, info):
        user = info.context.user
        
        if user.is_anonymous:
            raise Exception("Sepetinizi görüntülemek için lütfen token ile giriş yapın.")
            
        # get_or_create_basket from utils.py
        basket = get_or_create_basket(user)
        return basket

    # Resolver for favs
    def resolve_my_favorites(self, info):
        user = info.context.user

        if user.is_anonymous:
            raise Exception("Favorilerinizi görmek için giriş yapmalısınız.")

        return Favorite.objects.filter(user=user).select_related('product')


