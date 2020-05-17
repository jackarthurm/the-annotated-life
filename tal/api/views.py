from http import HTTPStatus
from typing import (
    Optional,
    Dict,
    Any,
    Tuple,
    Literal,
)

from flask import (
    request,
    current_app as app,
    url_for,
)
from flask.views import MethodView
from flask_sqlalchemy import Pagination

from tal.api.models import (
    Post,
    Author,
    db,
)
from tal.api.schemas import (
    PostSummarySchema,
    AuthorSchema,
    PostSchema,
)


class NamedResourceView(MethodView):
    """A named resource view can be reversed easily to enable HATEOAS URL
    linking, but names must be unique in the API.
    """

    name: str

    @classmethod
    def as_view(cls):
        return super().as_view(cls.name)

    @classmethod
    def reverse(cls, **values) -> str:
        return url_for(cls.name, **values)


class AuthorResource(NamedResourceView):

    name = 'author_detail_resource'

    def get(self, pk: str) -> Dict[str, Any]:

        author: Author = Author.query.get_or_404(pk)

        return dict(
            authors=AuthorSchema().dump(
                dict(
                    object_id=author.object_id,
                    object_url=self.reverse(
                        pk=author.object_id,
                        _external=True
                    ),
                    name=author.name,
                    media_url=author.media_url,
                    organisation_name=author.organisation,
                    organisation_url=author.organisation_url
                )
            )
        )

    def delete(self, pk: str) -> Tuple[Literal[''], HTTPStatus]:

        author: Author = Author.query.get_or_404(pk)
        db.session.delete(author)
        db.session.commit()

        return '', HTTPStatus.NO_CONTENT

    def put(self, pk: str) -> Tuple[Dict[str, Any], HTTPStatus]:

        object_data: Optional[Dict[str, Any]] = request.json

        if object_data is None:
            return dict(error='must be JSON'), HTTPStatus.NOT_ACCEPTABLE

        object_data['object_id'] = pk

        schema: AuthorSchema = AuthorSchema()

        author, errors = schema.load(
            object_data,
            partial=False
        )

        db.session.add(author)
        db.session.commit()

        return schema.dump(author), HTTPStatus.NO_CONTENT


class AuthorListResource(NamedResourceView):

    name = 'author_list_resource'

    def get(self) -> Dict[str, Any]:

        schema: AuthorSchema = AuthorSchema(many=True)

        # Make a paginated query
        page: str = request.args.get('page', '1')
        page: Optional[int] = int(page) if page.isdigit() else None

        page_size: str = app.config['PAGE_SIZE']
        page: Pagination = Author.query.paginate(page, page_size)

        return dict(
            authors=schema.dump(
                [
                    dict(
                        object_id=author.object_id,
                        object_url=AuthorResource.reverse(
                            pk=author.object_id,
                            _external=True
                        ),
                        name=author.name,
                        media_url=author.media_url,
                        organisation_name=author.organisation,
                        organisation_url=author.organisation_url
                    )
                    for author in page.items
                ]
            )
        )

    def post(self) -> Tuple[Dict[str, Any], HTTPStatus]:

        schema: AuthorSchema = AuthorSchema()

        request_data: Optional[Dict[str, Any]] = request.json

        if request_data is None:
            return dict(error='must be JSON'), HTTPStatus.NOT_ACCEPTABLE

        author, errors = schema.load(request_data, partial=False)

        if errors:
            return errors, HTTPStatus.BAD_REQUEST

        db.session.add(author)
        db.session.commit()

        return schema.dump(author), HTTPStatus.CREATED


class PostResource(NamedResourceView):

    name = 'post_detail_resource'

    def get(self, pk: str) -> Dict[str, Any]:

        schema: PostSchema = PostSchema()

        post: Post = Post.query.get_or_404(pk)

        return schema.dump(
            dict(
                object_id=post.object_id,
                object_url=self.reverse(
                    pk=post.object_id,
                    _external=True
                ),
                title_text=post.title,
                date_published=post.date_published,
                date_written=post.date_written,
                summary_text=post.summary,
                footer_text=post.footer,
                author_url=AuthorResource.reverse(
                    pk=post.author_id,
                    _external=True
                ),
                author_id=post.author_id,
                tags=post.tags,
                body_text=post.body,
                references=post.references
            )
        )

    def delete(self, pk: str) -> Tuple[Literal[''], HTTPStatus]:

        post: Post = Post.query.get_or_404(pk)
        db.session.delete(post)
        db.session.commit()

        return '', HTTPStatus.NO_CONTENT

    def put(self, pk: str) -> Tuple[Dict[str, Any], HTTPStatus]:

        object_data: Optional[Dict[str, Any]] = request.json

        if object_data is None:
            return dict(error='must be JSON'), HTTPStatus.NOT_ACCEPTABLE

        object_data['object_id'] = pk

        schema: PostSchema = PostSchema()

        post, errors = schema.load(
            object_data,
            partial=False
        )

        db.session.add(post)
        db.session.commit()

        return schema.dump(post), HTTPStatus.NO_CONTENT


class PostListResource(NamedResourceView):

    name = 'post_list_resource'

    def get(self) -> Dict[str, Any]:

        schema: PostSummarySchema = PostSummarySchema(many=True)

        # Make a paginated query
        page: str = request.args.get('page', '1')
        page: Optional[int] = int(page) if page.isdigit() else None

        page_size: str = app.config['PAGE_SIZE']
        page: Pagination = Post.query.paginate(page, page_size)

        return dict(
            posts=schema.dump(
                [
                    dict(
                        object_id=post.object_id,
                        object_url=PostResource.reverse(
                            pk=post.object_id,
                            _external=True
                        ),
                        title_text=post.title,
                        date_published=post.date_published,
                        date_written=post.date_written,
                        summary_text=post.summary,
                        footer_text=post.footer,
                        author_url=AuthorResource.reverse(
                            pk=post.author_id,
                            _external=True
                        ),
                        author_id=post.author_id,
                        tags=post.tags,
                    )
                    for post in page.items
                ]
            )
        )

    def post(self) -> Tuple[Dict[str, Any], HTTPStatus]:

        schema: PostSchema = PostSchema()

        object_data: Optional[Dict[str, Any]] = request.json

        if object_data is None:
            return dict(error='must be JSON'), HTTPStatus.NOT_ACCEPTABLE

        post, errors = schema.load(object_data, partial=False)

        if errors:
            return errors, HTTPStatus.BAD_REQUEST

        db.session.add(post)
        db.session.commit()

        return schema.dump(
            dict(
                object_id=post.object_id,
                object_url=PostResource.reverse(
                    pk=post.object_id,
                    _external=True
                ),
                title_text=post.title,
                date_published=post.date_published,
                date_written=post.date_written,
                summary_text=post.summary,
                footer_text=post.footer,
                author_url=AuthorResource.reverse(
                    pk=post.author_id,
                    _external=True
                ),
                author_id=post.author_id,
                tags=post.tags,
            )
        ), HTTPStatus.CREATED
