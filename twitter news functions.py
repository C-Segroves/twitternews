# -*- coding: utf-8 -*-
"""
Created on Sat Feb 26 22:57:19 2022

@author: Chris
"""

# Setup access to API

def connect_to_twitter_OAuth():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

    api = tweepy.API(auth, wait_on_rate_limit=True)
    return api

def get_user_friends(api,screen_name):
    friends=[]
    user = api.get_user(screen_name=screen_name)

    for friend in user.friends(count=200):
        friends.append(friend.screen_name)
    return(friends)

def get_user_tweets(api,screen_name,tweet_count=20):
    user = api.get_user(screen_name=screen_name)
    tweets = api.user_timeline(screen_name=screen_name, 
                           # 200 is the maximum allowed count
                           count=tweet_count,
                           include_rts = False,
                           # Necessary to keep full_text 
                           # otherwise only the first 140 words are extracted
                           tweet_mode = 'extended'
                           )
    return(tweets)

def pull_tweets_to_df(user_name,api):
    friends = get_user_friends(api,user_name)
    tweets_dict={'Friend':[],'Time_Stamp':[],'Tweet_txt':[]}
    for friend in friends:
        try:
            tweets = get_user_tweets(api,friend,tweet_count=20)
            for tweet in tweets:
                try:
                    tweets_dict['Friend'].append(friend)
                    tweets_dict['Time_Stamp'].append(tweet.created_at)
                    tweets_dict['Tweet_txt'].append(tweet.full_text)
                except:
                    print('something went wrong storing the tweets')
            #print_users_tweets(friend,tweets)
        except:
            print('something went wrong with the tweets for a user')
    tweets_df=pd.DataFrame(tweets_dict)
    tweets_df=tweets_df.sort_values('Time_Stamp',ascending=False)
    return(tweets_df)

def print_tweets(tweets_df,num_to_display):
    for i in range(100):
        try:
            print(tweets_df['Friend'].iloc[i])
            print(tweets_df['Time_Stamp'].iloc[i])
            print(tweets_df['Tweet_txt'].iloc[i],'\n\n')
        except:
            print('error in printing tweets')# Setup access to API
