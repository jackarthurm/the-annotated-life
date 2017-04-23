from marshmallow_sqlalchemy import ModelSchema

from src.models import Post


class PostSchema(ModelSchema):

    class Meta:
        model = Post