# hn-responder
Script that replies to every @newsycombinator tweet with a link to the comments page

## Setup

Install Python modules `requests-oauthlib` and `python-firebase`:
```
pip install requests-oauthlib
pip install python-firebase
```

Create a Twitter app on https://apps.twitter.com/app/

Get tokens and secrets for your app on "Keys and Access Tokens" page.

Create file `twitter-secrets.json` with following contents (replace with your actual tokens and secrets):
```
{
    "access_token": "12345",
    "access_token_secret": "abcdefg",
    "consumer_key": "1q2w3e4",
    "consumer_secret": "ABCDEFG"
}
```

Execute script from command line. Note that it will run forever until killed.
```
python hn-responder.py
```
