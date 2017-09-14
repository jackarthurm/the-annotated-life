from http.client import (
    CREATED,
    BAD_REQUEST,
)

from flask_restful import (
    Resource,
    Api,
    request,
    current_app as app,
)

from tal.api.schemas import (
    post_summary_list_schema,
    post_schema,
    author_schema,
    author_list_schema,
)


rest = Api()


class PostListResource(Resource):

    def get(self):
        return {
            'posts': dump_all_objects(post_summary_list_schema)
        }

    def post(self):

        obj, errors = load_object(post_schema)

        if errors:
            return errors, BAD_REQUEST

        obj.save()

        return post_schema.dump(obj).data, CREATED


class PostResource(Resource):

    def get(self, pk):
        return dump_object(post_schema, pk)

    def delete(self, pk):
        raise NotImplementedError

    def put(self, pk):
        raise NotImplementedError


class AuthorListResource(Resource):

    def get(self):
        return {
            'authors': dump_all_objects(author_list_schema)
        }

    def post(self):

        obj, errors = load_object(author_schema)

        if errors:
            return errors, BAD_REQUEST

        obj.save()

        return author_schema.dump(obj).data, CREATED


class AuthorResource(Resource):

    def get(self, pk):
        return dump_object(author_schema, pk)

    def delete(self, pk):
        raise NotImplementedError

    def put(self, pk):
        raise NotImplementedError


# Posts and post summaries
post_route = '/posts/'

rest.add_resource(PostListResource,
                  post_route)

rest.add_resource(PostResource,
                  post_route + '<string:pk>/')


# Authors
author_route = '/authors/'

rest.add_resource(AuthorListResource,
                  author_route)

rest.add_resource(AuthorResource,
                  author_route + '<string:pk>/')


def dump_all_objects(schema):

    model = schema.Meta.model

    # Paginate the queryset
    page = request.args.get('page', '1')
    page = int(page) if page.isdigit() else None

    page_size = app.config['PAGE_SIZE']

    query = model.query.paginate(page, page_size).items

    return schema.dump(query).data


def dump_object(schema, pk):

    model = schema.Meta.model

    query = model.query.get_or_404(pk)

    return schema.dump(query).data


def load_object(schema, partial=False):

    request_data = request.get_json(force=True)  # Ignore mimetype

    obj, errors = schema.load(request_data, partial=partial)

    return obj, errors
