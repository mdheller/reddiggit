from flask import Blueprint, flash, redirect, url_for, render_template, abort, g, request
from jinja2 import TemplateNotFound
import base36

bp = Blueprint('post', __name__, template_folder='templates')

class Post(object):
	def __init__(self, post_id, author, topic, votes=0):
		self.post_id = post_id
		self.author = author
		self.topic = topic
		self.votes = votes

posts=[]

@bp.route('/')
def index():
    try:
        return render_template('index.html', posts=posts)
    except TemplateNotFound:
        abort(404)

@bp.route('/submit', methods=['GET', 'POST'])
def add_post():
	if request.method == 'POST':
		#Topic should not exceed 255 characters.
		if len(request.values['topic']) > 255 :
			abort(400)
		new_post = Post(base36.dumps(len(posts)), request.values['author'], request.values['topic'])
		posts.append(new_post)
		flash("Post %s added" % new_post.post_id)
		return redirect(url_for('.index'))

@bp.route('/<post_id>/<action>')
def vote_post(post_id, action):
	p = posts[base36.loads(post_id)]
	if action=='upvote':
		p.votes +=1
	elif action=='downvote':
		p.votes -=1
	return redirect(url_for('.index'))
