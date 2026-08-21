import graphene
from app1.models import Comment
from app1.input import DeleteCommentInput

class DeleteComment(graphene.Mutation):
    class Arguments:
        data = DeleteCommentInput(required=True)

    message = graphene.String()
    success = graphene.Boolean()

    def mutate(self, info, data):
        user = info.context.user

        if user.is_anonymous:
            raise Exception("Yorum silmek için giriş yapmalısınız.")

        try:
            comment = Comment.objects.get(id=data.comment_id)
        except Comment.DoesNotExist:
            raise Exception("Silinmek istenen yorum bulunamadı.")

        # Kullanıcı sadece kendi yorumunu silebilir
        if comment.user != user:
            raise Exception("Yalnızca kendi yaptığınız yorumları silebilirsiniz.")

        comment.delete()

        return DeleteComment(
            message="Yorum başarıyla silindi.",
            success=True
        )