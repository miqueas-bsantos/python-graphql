# flask_sqlalchemy/schema.py
import graphene
from graphene import relay, Field, ID
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from ...models import db_session, UserModel, PostModel, HobbyModel
from ..post import Post, CreatePost
from graphene_sqlalchemy_filter import FilterableConnectionField, FilterSet

class User(SQLAlchemyObjectType):
    class Meta:
        model = UserModel
        interfaces = (relay.Node, )
        # connection_field_factory = CustomField.factory

class UserFilter(FilterSet):
    # is_admin = graphene.Boolean()
    class Meta:
        model = UserModel
        fields = {
            'id': ['eq'],
            'name': ['eq', 'ne', 'in', 'ilike'],
            'age': [...],  # shortcut!
        }

class Hobby(SQLAlchemyObjectType):
    class Meta:
        model = HobbyModel
        interfaces = (relay.Node, )

class Query(graphene.ObjectType):
    node = relay.Node.Field()
    # Allows sorting over multiple columns, by default over the primary key
    # all_users = SQLAlchemyConnectionField(User.connection)
    all_users = FilterableConnectionField(User.connection, filters=UserFilter(), sort=None)
    # Disable sorting over this field
    all_posts = FilterableConnectionField(Post.connection, filters=UserFilter(), sort=None)
    all_hobbies = SQLAlchemyConnectionField(Hobby.connection, sort=None)

class Mutation(graphene.ObjectType):
    create_user = CreatePost.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)