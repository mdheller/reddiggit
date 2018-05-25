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
    response = client.post('/post/submit', data=dict(
        author='test_upvote',
        topic='Usagi'
    ))
    assert response.status_code == 302
    a=[i.votes for i in filter(lambda x: x.topic=='Usagi' ,post.posts)]
    print a[0]
    rv = client.get('/post/0/upvote')
    assert rv.status_code== 302

def test_downvote(client):
    response = client.post('/post/submit', data=dict(
        author='test_downvote',
        topic='Pikachu'
    ))
    rv = client.get('/post/0/downvote')
    assert rv.status_code == 302
