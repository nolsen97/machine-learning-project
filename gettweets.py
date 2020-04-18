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
t = api.user_timeline(screen_name="realDonaldTrump", count=200, tweet_mode='extended')

tweets = []
for tweet in t:
    if 'https://t.co' in tweet.full_text:
        continue
    if tweet.full_text[0:2] == 'RT':
        tweets.append(tweet.retweeted_status.full_text)
    else:
        tweets.append(tweet.full_text)

#len(tweets)
#print(tweets)
file = open("tweets.txt", "w")

for i in tweets:
    i = i.replace('\n', ' ')
    file.write(i.lower())
    file.write('\n')

file.close()
