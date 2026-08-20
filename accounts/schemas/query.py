import graphene
from accounts.output import UserType

class UserQueries(graphene.ObjectType):
    me = graphene.Field(UserType)

    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Bu veriyi görmek için giriş yapmalısınız!")
        return user