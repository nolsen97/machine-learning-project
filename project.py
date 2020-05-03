# Following the following guide:

import pandas as pd
import datetime
import word2vec

"""
The idea:

For each day of the stock market, look at tweets made the day before
Use a library (maybe word2vec?) and pick out the key words from the tweet
If stock market goes up, label these words positively
if stock market goes down, label these words negatively

Train on 70%, Test on 30%
"""

def setupDF(tweets, df):
    df['Diff'] = df['Adj Close'] - df['Open']

    #for i in df['Diff']:
    #    print(i)

    tweets['date'] = tweets['date'].dt.date
    df['Date'] = df['Date'].dt.date

    #len(tweets['date'])

    tweets['stock_mov'] = 1122 * [0]

    # Creates a column in tweets dataframe that assigns the stock movement to the previous days tweets (days where the sotck market was closed are 0)
    diff1 = datetime.timedelta(days=1)
    for i in range(len(df['Date'])):
        prev_day = df['Date'].loc[i] - diff1
        tweets.loc[tweets['date'] == prev_day, 'stock_mov'] = df['Diff'].loc[i]


    # Randomize order
    tweets = tweets.sample(frac=1).reset_index(drop=True)

    return tweets



# TRAINING
# might want to group all @s and videos together!

def train(tweets):
    words_weight = {}

    for i in tweets['text'][0:800]:
        for j in i.split():
            if j not in words_weight:
                words_weight[j] = 0.01 * tweets.loc[tweets['text'] == i, 'stock_mov'].iloc[0]
            else:
                words_weight[j] += 0.01*tweets.loc[tweets['text'] == i, 'stock_mov'].iloc[0]

    return words_weight


# TESTING

def test(tweets, words_weight):

    model = word2vec.load('text8.bin')
    
    correct = 0
    wrong = 0
    for i in tweets['text'][800:]:
        guess = 0
        for j in i.split():
            if j in words_weight:
                guess += words_weight[j]
            else:
                try:
                    indexes, metrics = model.similar(j)
                    similar_words = model.generate_response(indexes, metrics).tolist()
                    for k in similar_words:
                        if k[0] in words_weight:
                            guess += words_weight[k[0]]
                            break
                    guess += 0
                except:
                    guess += 0
        #print(guess)
        if guess > 0:
            if tweets.loc[tweets['text'] == i, 'stock_mov'].iloc[0] > 0:
                correct += 1
            elif tweets.loc[tweets['text'] == i, 'stock_mov'].iloc[0] < 0:
                wrong += 1
            else:
                pass
        if guess < 0:
            if tweets.loc[tweets['text'] == i, 'stock_mov'].iloc[0] < 0:
                correct += 1
            elif tweets.loc[tweets['text'] == i, 'stock_mov'].iloc[0] > 0:
                wrong += 1
            else:
                pass

    print(correct)
    print(wrong)

    print(100*correct/(correct+wrong))


if __name__ == '__main__':
    tweets = pd.read_csv('tweets.csv', parse_dates= ['date'])
    df = pd.read_csv('^VIX.csv', parse_dates= ['Date'])

    tweets = setupDF(tweets, df)
    words_weight = train(tweets)
    test(tweets, words_weight)



