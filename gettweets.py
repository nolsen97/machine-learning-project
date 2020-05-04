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

#arr = []
#for status in tweepy.Cursor(api.user_timeline, screen_name="realDonaldTrump", tweet_mode='extended').items(20):
#    print(status.full_text)
#
#print(arr)

# t1 = api.user_timeline(screen_name="realDonaldTrump", count=200, max_id = 1252042796151017472, tweet_mode='extended')
# t2 = api.user_timeline(screen_name="realDonaldTrump", count=200, max_id = 1249042796151017472, tweet_mode='extended')
# t3 = api.user_timeline(screen_name="realDonaldTrump", count=200, max_id = 1246459270352207879, tweet_mode='extended')
# t4 = api.user_timeline(screen_name="realDonaldTrump", count=200, max_id = 1243312056805318656, tweet_mode='extended')
# t5 = api.user_timeline(screen_name="realDonaldTrump", count=200, max_id = 1241570447344447488, tweet_mode='extended')
# t6 = api.user_timeline(screen_name="realDonaldTrump", count=200, max_id = 1239201512171192321, tweet_mode='extended')

#print(t5[198].id)

# t = t1+t2[1:]+t3[1:]+t4[1:]+t5[1:]+t6[1:]

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

print(len(tweets))

df = pd.DataFrame({"text":tweets, "date":created_at})
df.date = df.date.dt.tz_localize('UTC').dt.tz_convert('US/Eastern')
df.to_csv('tweets.csv', index=False)
