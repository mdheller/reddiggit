from reddiggit import post

def test_submit(client, app):
    assert len(post.posts) == 0 
    response = client.post('/post/submit')
    assert response.data == b'Post added!'
    assert len(post.posts) == 1

def test_upvote(client):
    response = client.post('/post/submit')
    rv = client.get('/post/0/upvote')
    assert rv.data == b'post 0 +1.'

def test_downvote(client):
    response = client.post('/post/submit')
    rv = client.get('/post/0/downvote')
    assert rv.data == b'post 0 -1.'
