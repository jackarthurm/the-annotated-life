from marshmallow_sqlalchemy import ModelSchema

from tal.api.models import (db, 
                            Post)


class PostSchema(ModelSchema):

    class Meta:
        model = Post
        exclude = ['summary']
        sqla_session = db.session


post_schema = PostSchema()


class PostSummarySchema(ModelSchema):

    class Meta:
        model = Post
        exclude = ['body']
        sqla_session = db.session


post_summary_schema = PostSummarySchema(many=True)

