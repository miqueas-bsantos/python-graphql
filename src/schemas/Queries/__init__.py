# flask_sqlalchemy/schema.py
import graphene
from graphene import relay, Field, ID
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from ...models import db_session, UserModel, PostModel, HobbyModel
from graphene_sqlalchemy_filter import FilterableConnectionField, FilterSet

class PostFilter(FilterSet):
    # is_admin = graphene.Boolean()
    class Meta:
        model = PostModel
        fields = {
            'id': ['eq'],
            'comment': ['ilike']
        }

class CustomField(FilterableConnectionField):
    filters = {
        PostModel: PostFilter()
    }

class User(SQLAlchemyObjectType):
    class Meta:
        model = UserModel
        interfaces = (relay.Node, )
        connection_field_factory = CustomField.factory

class UserFilter(FilterSet):
    # is_admin = graphene.Boolean()
    class Meta:
        model = UserModel
        fields = {
            'id': ['eq'],
            'name': ['eq', 'ne', 'in', 'ilike'],
            'age': [...],  # shortcut!
        }

class Post(SQLAlchemyObjectType):
    class Meta:
        model = PostModel
        interfaces = (relay.Node, )

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
    
   

schema = graphene.Schema(query=Query)