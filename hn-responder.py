#!/usr/bin/python

import json
import re
import requests
from Queue import Queue
from requests_oauthlib import OAuth1
from threading import Thread
from firebase import firebase

with open('twitter-secrets.json') as twitter_secrets:
    s = json.load(twitter_secrets)
    access_token        = s['access_token']
    access_token_secret = s['access_token_secret']
    consumer_key        = s['consumer_key']
    consumer_secret     = s['consumer_secret']
auth = OAuth1(consumer_key, consumer_secret, access_token, access_token_secret)

firebase = firebase.FirebaseApplication(
    'https://hacker-news.firebaseio.com', None)

work_queue = Queue()


def read_tweets():
    url = 'https://userstream.twitter.com/1.1/user.json'
    r = requests.get(url, auth=auth, stream=True)
    for line in r.iter_lines():
        if line:
            tweet = json.loads(line.decode('utf-8'))
            work_queue.put(tweet)


def run():
    while True:
        tweet = work_queue.get()
        if 'user' in tweet and tweet['user']['id'] == 14335498:
            tweet_id = tweet['id']
            title = re.sub('https://t.co.*$', '', tweet['text']).strip()
            hackernews_id = find_hackernews_id(title)
            post_tweet(tweet_id, title, hackernews_id)
        work_queue.task_done()


def find_hackernews_id(title):
    top_ids = firebase.get('/v0/topstories', None)
    for item_id in top_ids:
        item = firebase.get('/v0/item', item_id)
        if 'title' in item and item['title'].strip() == title:
            return item_id


def trim_tweet(title, max_len):
    trimmed_title = title
    if len(title) > max_len:
        trimmed_title = title[:max_len - 3] + '...'
    return trimmed_title


def post_tweet(tweet_id, title, hackernews_id):
    url = 'https://api.twitter.com/1.1/statuses/update.json'
    trimmed_tweet = trim_tweet(title, 78)
    tweet_text = (
        'Comments to "' + trimmed_tweet + '"'
        ' https://news.ycombinator.com/item?id=' + str(hackernews_id) +
        ' https://twitter.com/newsycombinator/status/' + str(tweet_id))
    params = {'status': tweet_text}
    requests.post(url, auth=auth, data=params)


t = Thread(target=run)
t.daemon = True
t.start()

read_tweets()
work_queue.join()
