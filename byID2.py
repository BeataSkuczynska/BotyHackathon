# -*- coding: utf-8 -*-
"""
Created on Sun Jan 14 11:14:34 2018

@author: PC
"""

import tweepy
from settings import TWITTER

# Consumer keys and access tokens, used for OAuth
consumer_key = TWITTER["CONSUMER_KEY"]
consumer_secret = TWITTER["CONSUMER_SECRET"]
access_token = TWITTER["ACCESS_TOKEN"]
access_token_secret = TWITTER["ACCESS_TOKEN_SECRET"]

# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Creation of the actual interface, using authentication
api = tweepy.API(auth)

file = open("trump.txt", mode="w", encoding="UTF-8")
for status in tweepy.Cursor(api.user_timeline, screen_name='@realDonaldTrump').items(100):
    print(type(status))
    sjson = status._json['text']
    if "RT @" not in sjson:
        file.write(status._json['text'] + "\n")
        # print (status._json['text'])
        # print("\n")
file.close()