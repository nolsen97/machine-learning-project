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
    tweets.date = pd.to_datetime(tweets.date, utc=True)
    tweets['date'] = tweets['date'].dt.date
    df['Date'] = df['Date'].dt.date

    #len(tweets['date'])

    tweets['stock_mov'] = 3029 * [0]

    # Creates a column in tweets dataframe that assigns the stock movement to the previous days tweets (days where the sotck market was closed are 0)
    diff1 = datetime.timedelta(days=1)
    for i in range(len(df['Date'])):
        prev_day = df['Date'].loc[i] - diff1
        tweets.loc[tweets['date'] == prev_day, 'stock_mov'] = df['Diff'].loc[i]


    # Randomize order
    # Not sure if we should add a seed here so that the reandomization is always the same?
    tweets = tweets.sample(frac=1).reset_index(drop=True)

    return tweets



# TRAINING

def train(tweets):
    counter = 0
    words_weight = {}

    model = word2vec.load('text8.bin')

    for i in tweets['text'][0:2200]:
        counter += 1
        if counter in [220, 220*2, 220*3, 220*4, 220*5, 220*6, 220*7, 220*8, 220*9]:
            print(str(100*(counter/2200)) + "%" + " complete")

        for j in i.split():
            if j not in words_weight:
                words_weight[j] = 0.01 * tweets.loc[tweets['text'] == i, 'stock_mov'].iloc[0]
            else:
                words_weight[j] += 0.01*tweets.loc[tweets['text'] == i, 'stock_mov'].iloc[0]
            try:
                indexes, metrics = model.similar(j)
                similar_words = model.generate_response(indexes, metrics).tolist()
                for k in similar_words:
                    if k[0] not in words_weight:
                        words_weight[k[0]] = k[1] * 0.01 * tweets.loc[tweets['text'] == i, 'stock_mov'].iloc[0]
                    else:
                        words_weight[k[0]] += k[1] * 0.01 * tweets.loc[tweets['text'] == i, 'stock_mov'].iloc[0]
            except:
                pass

    return words_weight


# TESTING

def test(tweets, words_weight):

    model = word2vec.load('text8.bin')

    correct = 0
    wrong = 0
    for i in tweets['text'][2200:]:
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
                            guess += k[1] * words_weight[k[0]]
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

    return correct, wrong


if __name__ == '__main__':
    tweets = pd.read_csv('tweets.csv', parse_dates= ['date'])
    df = pd.read_csv('^VIX.csv', parse_dates= ['Date'])

    tweets = setupDF(tweets, df)
    words_weight = train(tweets)
    print("Finished Training")
    correct, wrong = test(tweets, words_weight)

    print("Correct predictions: " + str(correct))
    print("Wrong predictions: " + str(wrong))

    print("Percentage of correct predictions: " + str(100*correct/(correct+wrong)))

    print("10 Most Positive Words:")
    top_pos_words = sorted(words_weight.items(), key=lambda x: x[1], reverse=True)
    for i in top_pos_words[:10]:
        print(i[0] + ": " + str(i[1]))

    print("10 Most negative Words:")
    top_neg_words = sorted(words_weight.items(), key=lambda x: x[1])
    for i in top_neg_words[:10]:
        print(i[0] + ": " + str(i[1]))

# ADD WORD2VEC IN TRAINING