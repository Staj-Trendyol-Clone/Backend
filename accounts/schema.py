import graphene
import graphql_jwt
from accounts.schemas.register import CreateUser 
from accounts.schemas.update_profile import UpdateProfile 
from .schemas.query import UserQueries

class Query(UserQueries, graphene.ObjectType):
    pass

class Mutation(graphene.ObjectType):
    # Doğrudan CreateUser mutasyonunu Field olarak bağlıyoruz
    create_user = CreateUser.Field()
    update_profile = UpdateProfile.Field()
    
    # Login JWT mutasyonları
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()