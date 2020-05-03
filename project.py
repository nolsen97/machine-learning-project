# Following the following guide:

import pandas as pd
import datetime
import word2vec

tweets = pd.read_csv('tweets.csv', parse_dates= ['date'])
sp500 = pd.read_csv('CL=F.csv', parse_dates= ['Date'])



"""
The idea:

For each day of the stock market, look at tweets made the day before
Use a library (maybe word2vec?) and pick out the key words from the tweet
If stock market goes up, label these words positively
if stock market goes down, label these words negatively

Train on 70%, Test on 30%
"""

sp500['Diff'] = sp500['Adj Close'] - sp500['Open']

#for i in sp500['Diff']:
#    print(i)

tweets['date'] = tweets['date'].dt.date
sp500['Date'] = sp500['Date'].dt.date

#len(tweets['date'])

tweets['stock_mov'] = 1122 * [0]

# Creates a column in tweets dataframe that assigns the stock movement to the previous days tweets (days where the sotck market was closed are 0)
diff1 = datetime.timedelta(days=1)
for i in range(len(sp500['Date'])):
    prev_day = sp500['Date'].loc[i] - diff1
    tweets.loc[tweets['date'] == prev_day, 'stock_mov'] = sp500['Diff'].loc[i]


# TRAINING
# might want to group all @s and videos together!
words_weight = {}
# 70% is up to 376
for i in tweets['text'][0:900]:
#    print(i)

    #print(tweets.loc[tweets['text'] == i, 'stock_mov'].iloc[0])
    for j in i.split():
        if j not in words_weight:
            words_weight[j] = 0.01 * tweets.loc[tweets['text'] == i, 'stock_mov'].iloc[0]
        else:
            words_weight[j] += 0.01*tweets.loc[tweets['text'] == i, 'stock_mov'].iloc[0]


model = word2vec.load('text8.bin')
# TESTING
correct = 0
wrong = 0
for i in tweets['text'][900:]:
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
                        # print(words_weight[k[0]])
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

#words_weight['pence']

#model = word2vec.load('text8.bin')

# for i in words_weight:
#     print(i, words_weight[i])

#indexes, metrics = model.similar("shelter")

#print(model.generate_response(indexes, metrics).tolist())


