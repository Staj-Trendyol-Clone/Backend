import graphene
from accounts.input import UpdateProfileInput
from accounts.output import UserType
from accounts.utils import set_attributes

class UpdateProfile(graphene.Mutation):
    class Arguments:
        data = UpdateProfileInput(required=True)

    user = graphene.Field(UserType)
    message = graphene.String()

    def mutate(self, info, data):
        user = info.context.user

        # 1. Giriş kontrolü (Token doğrulaması)
        if user.is_anonymous:
            raise Exception("Profilinizi güncellemek için giriş yapmalısınız.")

        # 2. Gelen verileri kullanıcı nesnesine dinamik olarak aktar
        set_attributes(user, data)
        
        # 3. Model validasyonu ve kaydetme
        user.full_clean()
        user.save()

        return UpdateProfile(
            user=user,
            message="Profil bilgileriniz başarıyla güncellendi."
        )