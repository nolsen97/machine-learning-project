import tweepy
from dotenv import load_dotenv
from os.path import join, dirname

dotenv_path = join(dirname(__file__), '.env')


consumer_key='scduzqDcGmW8fkoVtKMGoKtlb'
consumer_secret='W7LeGd9eNsIx6S6Y3Ll3Gw1oqLIzorVIUGJqnmqyR6jcTdW629'
access_token_key='1158826906512441344-K0aZGIVaq5PyuNfRmfBNH1S5mHVoAu'
access_token_secret='1SnreN2Y9lRpXWiSoZeR84EwaAIfCIRmrZnrWihveCQ6Y'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token_key, access_token_secret)

api = tweepy.API(auth)

#print(api.VerifyCredentials())
t = api.user_timeline(screen_name="realDonaldTrump", count=100, tweet_mode='extended')
tweets = [[tweet.full_text] for tweet in t]

for i in t:
    print(t['text'])

