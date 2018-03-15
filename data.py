import pandas as pd

import re
import json
import glob

from tokenize import preprocess
from collections import Counter
from textblob import TextBlob

class Twitter_Data():


#joining all the data sets
    def get_all(self):
        path = r'data/'
        all_files = glob.glob(path + "*.csv")
        list_frame = []
        twitter_data = pd.DataFrame()

        for file in all_files :
            dframe = pd.read_csv(file)
            list_frame.append(dframe)
            twitter_data = pd.concat(list_frame, ignore_index=True)
        return twitter_data
#A function to clean unnecessary information from tweet like # tags, @, url links,  RT
    def clean_tweet(self, tweet):

        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())


#Joining the datasets from 2017_11_01 to 2017_11_03

    def joining(self):
        tdf1 = pd.read_csv('data/2017_11_01.csv')
        tdf2 = pd.read_csv('data/2017_11_01.csv')
        tdf3 = pd.read_csv('data/2017_11_01.csv')

        frames = [tdf1, tdf2, tdf3]
        joined = pd.concat(frames)

        return joined

###A collection of mentions######

    def term_mentions(self):
        count_all = Counter()
        tweet_data = self.get_all()
        tweets = []
        tweets = tweet_data['text']

        for tweet in tweets:
            term_mention = [term for term in preprocess(tweet) if term.startswith('@')]
            count_all.update(term_mention)

        return count_all

####Accounts tweeting about Donald Trump#####  
    def trump_tweet(self):
        twitter_data = self.get_all()
        tweets = []
        lists = []
        tweets = twitter_data['text']
        trump_tweets = pd.DataFrame()
        for tweet in tweets:
            if re.search('@POTUS', tweet) or re.search('@realDonaldTrump', tweet):
                new = twitter_data[twitter_data['text'] == tweet]
                lists.append(new)
        trump_tweets = pd.concat(lists, ignore_index=True)
        return trump_tweets

####No. of tweets on Donald Trump including the RT##### 
    def trump_reference(self):
        term_mention = self.term_mentions()
        trump_reference = term_mention['@POTUS'] + term_mention['@realDonaldTrump']

        return trump_reference

####PErcentage of accounts tweeting about Donald Trump####
    def trump_reference_percentage(self, twitter_data):
        tweets = twitter_data['text']
        trump_tweet = self.trump_reference()
        print('Percentage of accounts tweeting about Trump: {}%'.format(100*(trump_tweet)/len(tweets)))

#####Frequency of accounts tweeting about Donald Trump#####   
    def order_by_frequency(self):
        #accounts referencing trump
        trump_reference = self.trump_tweet()

        trump_reference['frequency'] = trump_reference.groupby(by='screen_name')['text'].transform('count')

        return trump_reference.sort_values('frequency')
####A sentiment analysis of tweets about Donald Trump using TextBlob####    
    def positive_tweets(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity < 0:
            return 'negative'    
        return 'neutral'
        
    '''
    def agg_tweets(self):
        trump_reference = self.order_by_frequency()

        users = trump_reference['screen_name'] 
        ptweets = []

        for user in users:
            tweets = trump_reference[trump_reference['screen_name'] == user]['text']
            ptweets = self.positive_tweets(tweets)
    '''



def main():
    df = Twitter_Data()
    first_three_datasets = df.joining()
    print("Joining First three datasets : /n")
    print(first_three_datasets) 

    tweet = df.trump_tweet()
    print(tweet['text'])

    df.trump_reference_percentage(tweet)
    order = order_by_frequency()
    print(order)

    ptweets = []
    ntweets = []
    nu = []
    tweets = tweet['text']
    for tweet in tweets:
        p = df.positive_tweets(tweet)
        if p == 'positive':
            ptweets.append(p)
        elif p == 'negative':
            ntweets.append(p)
        else : nu.append(p)
    print('Percentage of positive tweets :{} %'.format(100*len(ptweets)/len(tweets)))
    
    
    

if __name__ == '__main__':
    main()


'''
Tweets referencing to Donald Trump
 % of accounts tweeting about Donald Trump
 Order accounts by the frequency of tweets about Donald Trump
 percentage of Donald Trump tweets that are positive in nature
percentage of accounts with more than 50% of positive tweets of Donald Trump
'''

