from flask import (Blueprint, 
                   jsonify,
                   request,
                   current_app as app)
from flask.views import MethodView


from tal.api.models import (db,
                            Post)
from tal.api.schemas import (post_schema,
                             post_summary_schema)

rest = Blueprint('src', __name__)


class PostAPI(MethodView):

  def get(self, post_id):

    if post_id is None:
        return jsonify({'posts': get_post_summaries()})

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

# Posts and post summaries
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


def get_post_summaries():

  page = request.args.get('page', '1')
  page = int(page) if page.isdigit() else None

  page_size = app.config['POSTS_LIST_PAGE_SIZE']

  query = Post.query.paginate(page, page_size).items

  return post_summary_schema.dump(query).data

def get_post(post_id):

  query = Post.query.get_or_404(post_id)
  return post_schema.dump(query).data
