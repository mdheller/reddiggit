import re
import pytest

from reddiggit import post

@pytest.mark.usefixtures('client')
class TestPostFunctions:

    def test_submit(self, client):
        """Test submit post."""
        assert len(post.posts) == 0
        response = client.post('/post/submit', data=dict(
            author='test_submit',
            topic='Pisuke'
        ), follow_redirects=True)

        #Check if topic in list.
        assert 'Pisuke' in response.data
        assert len(post.posts) == 1

@pytest.mark.usefixtures('client')
class TestVoteFuntions:

    def test_upvote(self, client):
        """Test upvote function."""
        rv = client.post('/post/submit', data=dict(
            author='test_upvote',
            topic='Usagi'
        ), follow_redirects=True)

        #Get post_id from flash message.
        p_id = re.search('Post added with id (\w)', rv.data).group(1)
        p = post.get_post_by_id(p_id)

        #Check if upvote increased.
        assert p.votes == 0
        upvote = client.get('/post/%s/upvote' % p_id)
        assert upvote.status_code== 302
        assert p.votes == 1

    def test_downvote(self, client):
        """Test downvote function."""
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


    def test_multi_upvote(self, client):
        """Test if allow user to upvote multiple times."""
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

    def test_multi_downvote(self, client):
        """Test if allow user to downvote multiple times."""
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

@pytest.mark.usefixtures('client')
class TestSortFunctions:

    def test_sort(self, client):
        """Test if descending sort is working."""
        assert len(post.posts) == 0
        for i in range(20):
            response = client.post('/post/submit', data=dict(
                author='sort_test',
                topic='No.%d' % i
            ), follow_redirects=True)

            #Get post_id from flash message.
            p_id = re.search('Post added with id (\w)', response.data).group(1)

            #Upvote posts 'N' times if it's the Nth post.
            for j in range(i):
                rv = client.get('/post/%s/upvote' % p_id )

        #Gather all posts votes in a list.
        list_of_votes = [p.votes for p in post.posts]

        #Check if the list is in descending order.
        assert all( x>=y for x,y in zip(list_of_votes,list_of_votes[1:]))

    def test_sort_after_submit(self, client):
        """Test if new posts are sorted as well."""
        assert len(post.posts) == 0

        for i in range(2):
            client.post('/post/submit', data=dict(
                author='sort_test',
                topic='No.%d' % i
            ), follow_redirects=True)

        client.get('/post/0/upvote')
        client.get('/post/1/downvote')

        response = client.post('/post/submit', data=dict(
                author='sort_test',
                topic='this topic should between post 0 and post 1'
            ), follow_redirects=True)

        p_id = re.search('Post added with id (\w)', response.data).group(1)

        #Gather all posts id in a list.
        list_of_ids = [p.post_id for p in post.posts]

        #Check if the new post is at second position
        assert list_of_ids.index(p_id) == 1