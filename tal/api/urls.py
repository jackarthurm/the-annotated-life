from flask import Flask

from tal.api.views import (
    AuthorResource,
    AuthorListResource,
    PostResource,
    PostListResource,
)


POSTS_ROUTE: str = '/posts/'
AUTHORS_ROUTE: str = '/authors/'


def init_app(app: Flask) -> None:

    app.add_url_rule(
        f'{POSTS_ROUTE}<string:pk>/',
        view_func=PostResource.as_view(),
        methods=['GET', 'PUT', 'DELETE']
    )

    app.add_url_rule(
        POSTS_ROUTE,
        view_func=PostListResource.as_view(),
        methods=['GET', 'POST']
    )

    app.add_url_rule(
        f'{AUTHORS_ROUTE}<string:pk>/',
        view_func=AuthorResource.as_view(),
        methods=['GET', 'PUT', 'DELETE']
    )

    app.add_url_rule(
        AUTHORS_ROUTE,
        view_func=AuthorListResource.as_view(),
        methods=['GET', 'POST']
    )
