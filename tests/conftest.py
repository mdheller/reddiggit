import pytest
from reddiggit import create_app, post

@pytest.fixture
def app(request):
    app = create_app({
        'TESTING': True,
    })
    yield app
    def fin():
        #Drop all post after each test.
        post.posts = []
    request.addfinalizer(fin)

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()
