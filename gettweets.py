# DO NOT RERUN THIS FILE

import tweepy
from dotenv import load_dotenv
from os.path import join, dirname
import os
import pandas as pd
import re
import time

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

consumer_key = os.getenv('consumer_key')
consumer_secret = os.getenv('consumer_secret')
access_token_key = os.getenv('access_token_key')
access_token_secret = os.getenv('access_token_secret')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token_key, access_token_secret)

api = tweepy.API(auth)

def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            time.sleep(15)

tweets = []
created_at = []
for tweet in limit_handled(tweepy.Cursor(api.user_timeline, screen_name="realDonaldTrump", tweet_mode='extended').items(5000)):
    if tweet.full_text[0:2] == 'RT':
        no_links = re.sub('(https://).*', '', tweet.retweeted_status.full_text)
        rmv_spec = re.sub('[^A-Za-z0-9 ]+', '', no_links)
        if rmv_spec != '':
            tweets.append(rmv_spec.replace('\n', ' ').lower())
    else:
        no_links = re.sub('(https://).*', '', tweet.full_text)
        rmv_spec = re.sub('[^A-Za-z0-9 ]+', '', no_links)
        if rmv_spec != '':
            tweets.append(rmv_spec.replace('\n', ' ').lower())
    if rmv_spec != '':
        created_at.append(tweet.created_at)


df = pd.DataFrame({"text":tweets, "date":created_at})
df.date = df.date.dt.tz_localize('UTC').dt.tz_convert('US/Eastern')
df.to_csv('tweets.csv', index=False)
