from flask import Blueprint, render_template, abort, g, request
from jinja2 import TemplateNotFound
import base36

bp = Blueprint('topic', __name__, template_folder='templates')

class Post(object):
	def __init__(self, post_id, author, topic, votes=0):
		self.post_id = post_id
		self.author = author
		self.topic = topic
		self.votes = votes
posts=[]

@bp.route('/')
def show():
    try:
        return render_template('index.html',posts=posts)
    except TemplateNotFound:
        abort(404)

@bp.route('/submit', methods=['GET', 'POST'])
def add_post():
	if request.method == 'POST':
		posts.append( Post(base36.dumps(len(posts)), 'allenh', "Post No.%d" % (len(posts)+1)))
		return 'Post added!'

@bp.route('/<post_id>/<action>')
def vote_post(post_id, action):
	if action=='upvote':
		return 'post %s +1.' % post_id
	elif action=='downvote':
		return 'post %s -1.' % post_id



