import re
import pytest

from reddiggit import post

@pytest.mark.usefixtures('client')
class TestNegative:

    def test_null_topic(self, client):
        """Test if error message shows when topic is null while posting."""
        assert len(post.posts) == 0
        response = client.post('/post/submit', data=dict(
            author='test_empty_topic'
        ), follow_redirects=True)
        assert response.status_code == 200
        assert len(post.posts) == 0
        assert "Post failed" in response.data

    def test_null_author(self, client):
        """Test if error message shows when author is null while posting."""
        assert len(post.posts) == 0
        response = client.post('/post/submit', data=dict(
            topic='neg_test'
        ), follow_redirects=True)
        assert response.status_code == 200
        assert len(post.posts) == 0
        assert "Post failed" in response.data

    def test_empty_topic(self, client):
        """Test if error message shows when topic is empty while posting."""
        assert len(post.posts) == 0
        response = client.post('/post/submit', data=dict(
            author='test_empty_topic',
            topic=''
        ), follow_redirects=True)
        assert response.status_code == 200
        assert len(post.posts) == 0
        assert "Post failed" in response.data

    def test_empty_author(self, client):
        """Test if error message shows when author is empty while posting."""
        assert len(post.posts) == 0
        response = client.post('/post/submit', data=dict(
            author='',
            topic='neg_test'
        ), follow_redirects=True)
        assert response.status_code == 200
        assert len(post.posts) == 0
        assert "Post failed" in response.data

    def test_both_empty(self, client):
        """Test if error message shows when both attribute are empty string."""
        assert len(post.posts) == 0
        response = client.post('/post/submit', data=dict(
            author='',
            topic=''
        ), follow_redirects=True)
        assert response.status_code == 200
        assert len(post.posts) == 0
        assert "Post failed" in response.data

    def test_both_null(self, client):
        """Test if error message shows when both attribute are Null."""
        assert len(post.posts) == 0
        response = client.post('/post/submit', follow_redirects=True)
        assert response.status_code == 200
        assert len(post.posts) == 0
        assert "Post failed" in response.data

    def test_topic_exceed_255(self, client):
        """Should return '400 Bad Request' when topic exceeds 255 chars"""
        assert len(post.posts) == 0
        response = client.post('/post/submit', data=dict(
            author='neg_test',
            # A 256 chars string
            topic='T'*256
        ), follow_redirects=True)
        assert response.status_code == 400
        assert len(post.posts) == 0

    def test_upvote_post_not_exist(self, client):
        """Should return '400 Bad Request' when upvote a post not exist"""
        response = client.get('/post/0/upvote') 
        assert response.status_code == 400

    def test_downvote_post_not_exist(self, client):
        """Should return '400 Bad Request' when downvote a post not exist"""
        response = client.get('/post/0/downvote') 
        assert response.status_code == 400
