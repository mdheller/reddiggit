import re
from reddiggit import post

def test_null_topic(client, app):
    assert len(post.posts) == 0
    response = client.post('/post/submit', data=dict(
        author='test_empty_topic'
    ), follow_redirects=True)
    assert response.status_code == 200
    assert len(post.posts) == 0
    assert "Post failed" in response.data

def test_null_author(client, app):
    assert len(post.posts) == 0
    response = client.post('/post/submit', data=dict(
        topic='neg_test'
    ), follow_redirects=True)
    assert response.status_code == 200
    assert len(post.posts) == 0
    assert "Post failed" in response.data

def test_empty_topic(client, app):
    assert len(post.posts) == 0
    response = client.post('/post/submit', data=dict(
        author='test_empty_topic',
        topic=''
    ), follow_redirects=True)
    assert response.status_code == 200
    assert len(post.posts) == 0
    assert "Post failed" in response.data

def test_empty_author(client, app):
    assert len(post.posts) == 0
    response = client.post('/post/submit', data=dict(
        author='',
        topic='neg_test'
    ), follow_redirects=True)
    assert response.status_code == 200
    assert len(post.posts) == 0
    assert "Post failed" in response.data

def test_both_empty(client, app):
    assert len(post.posts) == 0
    response = client.post('/post/submit', data=dict(
        author='',
        topic=''
    ), follow_redirects=True)
    assert response.status_code == 200
    assert len(post.posts) == 0
    assert "Post failed" in response.data

def test_both_null(client, app):
    assert len(post.posts) == 0
    response = client.post('/post/submit', follow_redirects=True)
    assert response.status_code == 200
    assert len(post.posts) == 0
    assert "Post failed" in response.data

def test_topic_exceed_255(client, app):
    assert len(post.posts) == 0
    response = client.post('/post/submit', data=dict(
        author='neg_test',
        # A 256 chars string
        topic='T'*256
    ), follow_redirects=True)
    assert response.status_code == 400
    assert len(post.posts) == 0

def test_upvote_post_not_exist(client, app):
    response = client.get('/post/0/upvote') 
    assert response.status_code == 400

def test_downvote_post_not_exist(client, app):
    response = client.get('/post/0/downvote') 
    assert response.status_code == 400
