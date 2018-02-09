# -*- coding: utf-8 -*-
"""
This script is for downloading tweets to TXT file from particular Twitter account.
"""
# NOTE: Working direcgory must be set to ..\boty_hackathon\

import tweepy
from settings import TWITTER
import argparse


def get_twitter_api():
    consumer_key = TWITTER["CONSUMER_KEY"]
    consumer_secret = TWITTER["CONSUMER_SECRET"]
    access_token = TWITTER["ACCESS_TOKEN"]
    access_token_secret = TWITTER["ACCESS_TOKEN_SECRET"]

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api


def download_tweets(path, amount_of_tweets, user_name):
    api = get_twitter_api()
    with open(path + user_name[1:] + ".txt", 'a', encoding="UTF-8") as file:
        for status in tweepy.Cursor(api.user_timeline, screen_name=user_name).items(int(amount_of_tweets)):
            sjson = status._json['text']
            if "RT @" not in sjson:
                file.write(status._json['text'] + "\n")
    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download tweets from particular account')
    parser.add_argument('path_to_save_tweets', help='the path to directory to save tweets', default="resources/")
    parser.add_argument('number_of_tweets', help='how many tweets download')
    parser.add_argument('user_name', help="'@' followed by user name")

    args = parser.parse_args()
    download_tweets(args.path_to_save_tweets, args.number_of_tweets, args.user_name)
