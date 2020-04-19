# DO NOT RERUN THIS FILE

import tweepy
from dotenv import load_dotenv
from os.path import join, dirname
import os
import pandas as pd

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

consumer_key = os.getenv('consumer_key')
consumer_secret = os.getenv('consumer_secret')
access_token_key = os.getenv('access_token_key')
access_token_secret = os.getenv('access_token_secret')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token_key, access_token_secret)

api = tweepy.API(auth)

t1 = api.user_timeline(screen_name="realDonaldTrump", count=200, tweet_mode='extended')
t2 = api.user_timeline(screen_name="realDonaldTrump", count=200, max_id = 1249042796151017472, tweet_mode='extended')
t3 = api.user_timeline(screen_name="realDonaldTrump", count=200, max_id = 1246459270352207879, tweet_mode='extended')
t4 = api.user_timeline(screen_name="realDonaldTrump", count=200, max_id = 1243312056805318656, tweet_mode='extended')

t = t1+t2[1:]+t3[1:]+t4[1:]

tweets = []
created_at = []
for tweet in t:
    if 'https://t.co' in tweet.full_text:
        continue
    if tweet.full_text[0:2] == 'RT':
        tweets.append(tweet.retweeted_status.full_text.replace('\n', ' ').lower())
    else:
        tweets.append(tweet.full_text.replace('\n', ' ').lower())
    created_at.append(tweet.created_at)

df = pd.DataFrame({"text":tweets, "date":created_at})
df.date = df.date.dt.tz_localize('UTC').dt.tz_convert('US/Eastern')
df.to_csv('tweets.csv', index=False)

"""
file = open("tweets.txt", "w")

for i, j in zip(tweets, created_at):
    text = i.replace('\n', ' ')
    file.write(text.lower() + ' :: ' + str(j))
    file.write('\n')

file.close()
"""