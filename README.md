# reddiggit
A Reddit / Digg clone with upvote and downvotes.
Build with Flask.

## Prerequisites
To build and run this application, you will need:

1.  Python version 2.7.9 (or higher)
2. [Virtualenv](https://virtualenv.pypa.io/en/stable/)

----
## Build Instructions
    git clone https://github.com/w84miracle/reddiggit
    cd reddiggit/
    virtualenv venv
    . venv/bin/activate
    pip install -r requirements.txt
    export FLASK_APP=reddiggit
    export FLASK_APP=development
    flask run

Visit [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

## Documentation
* Both user and topic field can't be empty.
* Topic should not exceeds 255 characters, which is handled in both frontend and backend.
* Like Reddit, user can upvote/downvote a topic by clicking arrows on the left of each topics.
* In-memory: All posts are store in a Python list.  **Hence all topics will disappear after the application restarts.**
* Posts will be given a unique id on submissions to identify each post. Which is a base 36 encoding text. (Like Reddit's [fullnames](https://www.reddit.com/dev/api/))
* Sorting may take a some time when the list getting bigger. So  instead of sorting the list each time user reaches index page, it will only sort on each submission and vote happens.

----
##Testing
run pytest
