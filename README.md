# hn-responder

A Python script that replies to every @newsycombinator tweet with a link to the article's comments page.

<div style="text-align:center">
<img src="https://cloud.githubusercontent.com/assets/344615/24843774/c6d5855a-1d5a-11e7-86ef-263e2dc1c581.png" style="width:500px;">
</div>

This script uses the Twitter API and Hacker News API via Firebase. It reads all tweets for the authenticated Twitter account and puts them into a queue. A background thread takes the tweets from the queue. If a tweet is from the @newsycombinator Twitter account, the background thread goes through all top Hacker News articles via the Firebase API and selects the article that matches the title of the tweet. It then sends out a reply tweet with the link to the article's comments page.

## Setup

To run the script, use the following steps:

1. Install the Python modules `requests-oauthlib` and `python-firebase`:

        pip install requests-oauthlib
        pip install python-firebase

1. Create a Twitter app on https://apps.twitter.com/app/.  Get the tokens and secrets for your Twitter app on the "Keys and Access Tokens" page.́
1. Create file `twitter-secrets.json` with following contents (replace with your actual tokens and secrets):

        {
            "access_token": "12345",
            "access_token_secret": "abcdefg",
            "consumer_key": "1q2w3e4",
            "consumer_secret": "ABCDEFG"
        }
1. Execute script `hn-responder.py` from the command line. Note that it will run forever until killed.

        python hn-responder.py
