
import graphene
from ...models import db_session, UserModel, PostModel, HobbyModel
from graphene_sqlalchemy_filter import FilterableConnectionField, FilterSet
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from graphene import relay, Mutation

class Post(SQLAlchemyObjectType):
    class Meta:
        model = PostModel
        interfaces = (relay.Node, )

class PostFilter(FilterSet):
    # is_admin = graphene.Boolean()
    class Meta:
        model = PostModel
        fields = {
            'id': ['eq'],
            'comment': ['ilike']
        }

class CreatePost(Mutation):

    class Arguments:
        comment = graphene.String(required=True, description="The user comment in the post")
        user_id = graphene.String(required=True)

    post = graphene.Field(Post)

    def mutate(root, info, comment, user_id):
        print(info)
        print(root)
        postCreate = PostModel(
                comment=comment,
                user_id=user_id
            )
        db_session.add(postCreate)
        db_session.commit()
        return CreatePost(post=postCreate)
    

class CustomField(FilterableConnectionField):
    filters = {
        PostModel: PostFilter()
    }
