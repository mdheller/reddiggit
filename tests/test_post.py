import re
from reddiggit import post

def test_submit(client, app):
    assert len(post.posts) == 0
    response = client.post('/post/submit', data=dict(
        author='test_submit',
        topic='Pisuke'
    ))
    assert response.status_code == 302
    assert len(post.posts) == 1

def test_upvote(client):
    rv = client.post('/post/submit', data=dict(
        author='test_upvote',
        topic='Usagi'
    ), follow_redirects=True)
    assert 'Usagi' in rv.data 
    p_id = re.search('Post added with id (\w)', rv.data).group(1)
    p = post.get_post_by_id(p_id)
    
    assert p.votes == 0
    upvote = client.get('/post/%s/upvote' % p_id)
    assert upvote.status_code== 302
    assert p.votes == 1 

def test_downvote(client):
    rv = client.post('/post/submit', data=dict(
        author='test_downvote',
        topic='Pikachu'
    ), follow_redirects=True)
    
    p_id = re.search('Post added with id (\w)', rv.data).group(1)
    p = post.get_post_by_id(p_id)
    
    assert p.votes == 0
    downvote = client.get('/post/%s/downvote' % p_id)
    assert downvote.status_code == 302
    assert p.votes == -1 


def test_multi_upvote(client):
    rv = client.post('/post/submit', data=dict(
        author='test_multi_upvote',
        topic='Multiple upvotes'
    ), follow_redirects=True)
    assert 'Multiple upvotes' in rv.data 
    p_id = re.search('Post added with id (\w)', rv.data).group(1)
    p = post.get_post_by_id(p_id)
    
    assert p.votes == 0
    for i in range(100):
       upvote = client.get('/post/%s/upvote' % p_id)
       assert upvote.status_code== 302
       assert p.votes == i+1

def test_multi_downvote(client):
    rv = client.post('/post/submit', data=dict(
        author='test_multi_downvote',
        topic='Multiple downvotes'
    ), follow_redirects=True)
    assert 'Multiple downvotes' in rv.data 
    p_id = re.search('Post added with id (\w)', rv.data).group(1)
    p = post.get_post_by_id(p_id)
    
    assert p.votes == 0
    for i in range(100):
       upvote = client.get('/post/%s/downvote' % p_id)
       assert upvote.status_code== 302
       assert p.votes == -(i+1)
