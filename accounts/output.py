from graphene_django import DjangoObjectType
from accounts.models import CustomUser

# Type  
class UserType(DjangoObjectType):
  class Meta:  
    model = CustomUser
    # disabled the accessibility of password for frontend
    fields = ("id", "username", "email", "phone_number", "birth_date", "address")
