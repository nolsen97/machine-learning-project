# Following the following guide:

import pandas as pd

tweets = pd.read_csv('tweets.csv')
sp500 = pd.read_csv('^GSPC.csv')

"""
The idea:

For each day of the stock market, look at tweets made the day before
Use a library (maybe word2vec?) and pick out the key words from the tweet
If stock market goes up, label these words positively
if stock market goes down, label these words negatively

Train on 70%, Test on 30%
"""

sp500['Diff'] = sp500['Adj Close'] - sp500['Open']

for i in sp500['Diff']:
    print(i)

