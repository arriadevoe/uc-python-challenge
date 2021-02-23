## Download 
We suggest we git clone this on your local envrionment and push to a new public repo on your account. 
We would prefer you don't fork to avoid other people being able to see your work easily.

## Install
```sh
pipenv install
```

## Shell
```sh
pipenv shell
```

## Run
```sh
flask run
```

## Task
You will be implementing a simplified passthrough api in flask. It will allow you to "login" as user (no password) get a web token that you use for other API calls. You will pass an API Token and query parameter to the other API. You will implement the following API endpoints.
- POST /login
- GET /user
- GET /widgets

You will also implement additional three functions. All functions and API endpoints that you will need to implement are in the app.py file with instructions on how they will work and hints on implementation.

Unit or automated tests aren't necessary unless they help you, we think they would add too much time commitment. Matt didn't end up using them for his implementation.

## Testing
We recomend using either curl or postman to test depending on whether you prefer console or UI.

## Time
Matt completed in about 45 minutes, so we are expecting it to take 1.5-2 hours for most candidates. You don't have to complete this assignment if you feel it is taking too long given your own definition of too long and if it takes more than 3-4 hours we strongly encourage you to leave it unfinished as it was not our intent. This assignment is not going to be used as a pass/fail assignment but rather as a conversation point in the in person interview, which may include pairing to improve the code in this assignment and pairing to finish the assignment would be equally valuable. Feel free to ask questions at any point.

## Submission 
We would ask that you send Matt a link to your repository before the interview, preferably at least 24 hours before.


## Terms of use by others for interviews
If you end up copying this and using it to conduct interviews you agree to remove/replace the reference to the external that this code test hits. It's run on a free plan of firebase and can't handle traffic coming from multiple companies interview processes. If you want the code for that other API log an issue on this repo and I'll post it.
