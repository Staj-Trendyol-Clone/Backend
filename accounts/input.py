import graphene

# Required infos from frontend:
class RegisterInput(graphene.InputObjectType):
    username = graphene.String(required=True) 
    password = graphene.String(required=True)
    email = graphene.String(required=True)
    phone_number = graphene.String()
    birth_date = graphene.Date()
    address = graphene.String()


class UpdateProfileInput(graphene.InputObjectType):
    username = graphene.String()
    phone_number = graphene.String()
    birth_date = graphene.String()
    address = graphene.String()     