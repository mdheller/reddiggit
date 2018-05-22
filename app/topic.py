class Topic(object):
	def __init__(self, topic, user, votes=0):
		self.topic = topic
		self.votes = votes
		self.user = user

@app.route('/topic/<post_id>', methods=['GET', 'POST'])
def add_topic(post_id):
	if request.method == 'POST':
		return 'Topic added!'
	else:
		return 'Topic %s' % post_id

@app.route('/topic/<post_id>/<action>')
def vote_topic(action):
	if action=='upvote':
		return 'topic %s +1.' % post_id
	elif action=='downvote':
		return 'topic %s -1.' % post_id



