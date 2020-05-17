from marshmallow import (
    ValidationError,
    validates,
    Schema,
    validate,
)
from marshmallow.fields import (
    Nested,
    URL,
    UUID,
    String,
    DateTime,
)


class BaseSchema(Schema):

    object_id = UUID(dump_only=True)
    object_url = URL(dump_only=True)


class AuthorSchema(BaseSchema):

    name = String(validate=validate.Length(max=100))
    media_url = URL()
    organisation_name = String(validate=validate.Length(max=100))
    organisation_url = URL()


class ReferenceSchema(BaseSchema):

    description = String(validate=validate.Length(max=300))
    post_url = URL(dump_only=True)
    post_id = UUID()


class TagSchema(BaseSchema):

    value = String(validate=validate.Length(max=40))
    post_url = URL(dump_only=True)
    post_id = UUID()


class PostSummarySchema(BaseSchema):

    title_text = String(validate=validate.Length(max=100))
    date_published = DateTime()
    date_written = DateTime()
    summary_text = String(validate=validate.Length(max=200))
    footer_text = String(validate=validate.Length(max=100))
    author_url = URL(dump_only=True)
    author_id = UUID()
    tags = Nested(TagSchema, many=True, dump_only=True)


class PostSchema(PostSummarySchema):

    body_text = String()
    references = Nested(ReferenceSchema, many=True)
