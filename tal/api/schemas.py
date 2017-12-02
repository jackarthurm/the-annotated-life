from uuid import UUID

from marshmallow import (
    ValidationError,
    validates,
)
from flask_marshmallow import Marshmallow

from tal.api.models import (
    Post,
    Author,
    Reference,
    Tag,
)


ma = Marshmallow()


class BaseSchema(ma.ModelSchema):

    class Meta:
        include_fk = True


class AuthorSchema(BaseSchema):

    class Meta(BaseSchema.Meta):
        model = Author


author_schema = AuthorSchema()
author_list_schema = AuthorSchema(many=True)


class ReferenceSchema(BaseSchema):

    class Meta(BaseSchema.Meta):
        model = Reference


class TagSchema(BaseSchema):

    class Meta(BaseSchema.Meta):
        model = Tag    


class PostSchema(BaseSchema):

    class Meta(BaseSchema.Meta):
        model = Post
        load_only = (
            'summary',
        )

    url = ma.AbsoluteURLFor(
        'postresource',
        pk='<id>',
    )

    tags = ma.Nested(TagSchema, many=True)
    references = ma.Nested(ReferenceSchema, many=True)

    author = ma.HyperlinkRelated(
        'authorresource',
        'pk',
        external=True,
    )

    @validates('author_id')
    def validate_author(self, value: UUID) -> None:
        if Author.query.get(value) is None:
            raise ValidationError('Invalid author id')


post_schema = PostSchema()


class PostSummarySchema(PostSchema):

    class Meta(BaseSchema.Meta):
        model = Post
        exclude = (
            'body',
            'references',
        )


post_summary_list_schema = PostSummarySchema(many=True)
