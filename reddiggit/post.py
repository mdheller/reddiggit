from flask import Blueprint, flash, redirect, url_for, render_template, abort, request
from jinja2 import TemplateNotFound
from datetime import datetime
import base36

bp = Blueprint('post', __name__, template_folder='templates')

class Post(object):
    """Class for storing informations from post that users submitted.
    Attributes:
        post_id (str): A base36 encoding (same as Reddit) text which
            represents serial number of each posts on created.
        author (str): User who submitted this post.
        topic (str): The topic from user's input, should not exceeds 255
            characters according to the requirement.
        votes (int): The total number of upvote - downvote, default is 0.
        create_time (str): The string of datetime when user submmit this post.
    """

    def __init__(self, post_id, author, topic, votes=0):
        self.post_id = post_id
        self.author = author
        self.topic = topic
        self.votes = votes
        self.create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def __lt__(self, other):
        """Make instances of this class sortable by it's upvote."""
        return self.votes < other.votes

    def __eq__(self, other):
        return self.votes == other.votes

# 'posts' is a list contains all user posts in-memory.
posts=[]

def get_post_by_id(post_id):
    """Return a post object for a given post_id."""
    global posts
    for p in posts:
        if p.post_id == str(base36.loads(post_id)):
            break
    else:
        p = None

    return p

@bp.route('/')
def index():
    try:
        # Render index page with top 20 upvotes posts.
        return render_template('index.html', posts=posts[:20])
    except TemplateNotFound:
        abort(404)

@bp.route('/post/submit', methods=['POST'])
def add_post():
    author = request.form.get('author', None)
    topic = request.form.get('topic', None)

    if author and topic:
        # If topic exceeds 255 characters, return with 400 Bad Request.
        if len(topic) > 255 :
            abort(400)
        new_post = Post(base36.dumps(len(posts)), author, topic)
        # Append the new post and sort the posts by upvotes.
        posts.append(new_post)
        posts.sort(reverse=True)

        flash("Post added with id %s" % new_post.post_id)
    else:
        flash("Post failed, please fill both user and topic field above.")

    return redirect(url_for('.index'))

@bp.route('/post/<post_id>/<action>')
def vote_post(post_id, action):
    p = get_post_by_id(post_id)
    # If post can't be found with post_id, return 400 Bad Request.
    if p is None:
        abort(400)
    else:
        if action=='upvote':
            p.votes +=1
        elif action=='downvote':
            p.votes -=1
        # When upvote/downvote, sort the posts by upvotes, descending.
        posts.sort(reverse=True)

    return redirect(url_for('.index'))
