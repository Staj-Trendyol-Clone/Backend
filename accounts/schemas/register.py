import graphene
from accounts.models import CustomUser
from accounts.utils import set_attributes
from accounts.input import RegisterInput
from accounts.output import UserType
import jwt
from django.conf import settings
 


# Register
class CreateUser(graphene.Mutation):
  # We want the attributes from frontend
  class Arguments:
    data = RegisterInput(required=True)

  user = graphene.Field(UserType)
  token = graphene.String()

  def mutate(self, info, data):
    user = CustomUser()
    set_attributes(user, data)
    user.set_password(data.password)
    user.save()
    
    key = settings.SECRET_KEY
    algorithm = getattr(settings, 'JWT_ALGORITHM', 'HS256')
    payload = {'username': user.username}
    token = jwt.encode(payload, key, algorithm)

    return CreateUser(user=user, token=token)

# Mutation  
class RegisterMutation(graphene.ObjectType):
    create_user = CreateUser.Field()
   




