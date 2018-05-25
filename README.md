# reddiggit
A Reddit / Digg clone with upvote and downvotes.
Build with Flask.

Online demo on Heroku:  [https://reddiggit.herokuapp.com/](https://reddiggit.herokuapp.com/)

To build this app on your own, follow the section below.

## How to run this app locally?
### Prerequisites
To build and run this application locally, you will need:

1. Python version 2.7.9 (or higher)
2. [Virtualenv](https://virtualenv.pypa.io/en/stable/)

### Follow these commands

    git clone https://github.com/w84miracle/reddiggit
    cd reddiggit/
    virtualenv venv
    . venv/bin/activate
    pip install -r requirements.txt
    export FLASK_APP=reddiggit
    export FLASK_APP=development
    flask run

And this application should start running on [http://localhost:5000/](http://localhost:5000/).

## Testing Application
Tests using [pytest](https://pytest.org/). All the test cases are in the tests/ directory.

Execute `python -m pytest tests/` to run all the tests at once.

## Notes
### Post
* Informations about each post are storing in a class, which contains following attributes:
  * post_id (str): A unique string represent this post.
  * author (str): User who submitted this post.
  * topic (str): The topic from user's input.
  * votes (int): The number of *upvote - downvote*, default is 0.
  * create_time (str): The string of datetime when user submit this post.
* Neither *author* nor *topic* attribute can be empty.
* Topic should not exceeds 255 characters, which is handled in both [frontend](https://github.com/w84miracle/reddiggit/blob/master/reddiggit/templates/index.html#L71) and [backend](https://github.com/w84miracle/reddiggit/blob/master/reddiggit/post.py#L62-L64).
* Posts will be given a unique id on submissions to identify each post. Which is a base 36 encoding text. (Like Reddit's [fullnames](https://www.reddit.com/dev/api/))
* Like Reddit, user can upvote/downvote a topic by clicking arrows on the left of each topics.

### In-memory
* All posts are store in a Python list.  **Hence all topics will disappear after the application restarts.**

### Sorting
* Homepage will always show only top 20 posts, sorting descendingly by each post's upvote amount.
* Sorting may take a some time when the list getting bigger. So instead of sorting the list each time user reaches index page, it will only sort on each post submission or upvote/downvote happens.