from marshmallow_sqlalchemy import ModelSchema

from src.models import (db, 
                        Post)


class PostSchema(ModelSchema):

    class Meta:
        model = Post
        sqla_session = db.session

post_schema = PostSchema()
posts_schema = PostSchema(many=True)

