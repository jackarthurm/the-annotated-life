from flask import (Blueprint, 
                   jsonify,
                   request)
from flask.views import MethodView

from tal.api.models import (db,
                            Post)
from tal.api.schemas import (post_schema,
                             posts_schema)

rest = Blueprint('src', __name__)


class PostAPI(MethodView):

    def get(self, post_id):

        if post_id is None:
            return jsonify({'posts': get_all_posts()})

        else:
            return jsonify(get_post(post_id))

    def post(self):

        request_data = request.get_json(force=True)  # Ignore mimetype

        post_obj, errors = post_schema.load(request_data)

        if errors:
            return jsonify(errors), 400

        db.session.add(post_obj)
        db.session.commit()

        response_data = post_schema.dump(post_obj).data

        return jsonify(response_data)

    def delete(self, post_id):

        raise NotImplementedError

    def put(self, post_id):

        raise NotImplementedError


post_route = '/posts/'
post_view = PostAPI.as_view('post_api')

# Get posts list
rest.add_url_rule(post_route, 
                  defaults={'post_id': None}, 
                  view_func=post_view, 
                  methods=['GET'])

# Create a post
rest.add_url_rule(post_route, 
                  view_func=post_view, 
                  methods=['POST'])

# Read, update, or delete a specific post
rest.add_url_rule(post_route + '<int:post_id>/',
                  view_func=post_view, 
                  methods=['GET', 'PUT', 'DELETE'])


def get_all_posts():

    query = Post.query.all()
    return posts_schema.dump(query).data

def get_post(post_id):

    query = Post.query.get_or_404(post_id)
    return post_schema.dump(query).data
