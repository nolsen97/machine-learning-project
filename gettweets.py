import tweepy
from dotenv import load_dotenv
from os.path import join, dirname
import os

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

consumer_key = os.getenv('consumer_key')
consumer_secret = os.getenv('consumer_secret')
access_token_key = os.getenv('access_token_key')
access_token_secret = os.getenv('access_token_secret')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token_key, access_token_secret)

api = tweepy.API(auth)

#print(api.VerifyCredentials())
t1 = api.user_timeline(screen_name="realDonaldTrump", count=200, tweet_mode='extended')
t2 = api.user_timeline(screen_name="realDonaldTrump", count=200, max_id = 1248475288171761670, tweet_mode='extended')
t3 = api.user_timeline(screen_name="realDonaldTrump", count=200, max_id = 1245754978880241664, tweet_mode='extended')
t4 = api.user_timeline(screen_name="realDonaldTrump", count=200, max_id = 1242414528031227902, tweet_mode='extended')

t = t1+t2+t3[1:]+t4[1:]
len(t)
tweets = []
for tweet in t:
    if 'https://t.co' in tweet.full_text:
        continue
    if tweet.full_text[0:2] == 'RT':
        tweets.append(tweet.retweeted_status.full_text)
    else:
        tweets.append(tweet.full_text)

file = open("tweets.txt", "w")

for i in tweets:
    i = i.replace('\n', ' ')
    file.write(i.lower())
    file.write('\n')

file.close()