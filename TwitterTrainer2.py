import logging
import os
import sys
from chatterbot.conversation import Statement, Response
from chatterbot.utils import print_progress_bar
from chatterbot.trainers import Trainer


class TwitterTrainers(Trainer):
    """
    Allows the chat bot to be trained using data
    gathered from Twitter.

    :param random_seed_word: The seed word to be used to get random tweets from the Twitter API.
                             This parameter is optional. By default it is the word 'random'.
    :param twitter_lang: Language for results as ISO 639-1 code.
                         This parameter is optional. Default is None (all languages).
    """

    def __init__(self, storage, **kwargs):
        super(TwitterTrainers, self).__init__(storage, **kwargs)
        from twitter import Api as TwitterApi

        # The word to be used as the first search term when searching for tweets
        self.random_seed_word = kwargs.get('random_seed_word', 'random')
        self.lang = kwargs.get('twitter_lang')

        self.api = TwitterApi(
            consumer_key=kwargs.get('twitter_consumer_key'),
            consumer_secret=kwargs.get('twitter_consumer_secret'),
            access_token_key=kwargs.get('twitter_access_token_key'),
            access_token_secret=kwargs.get('twitter_access_token_secret')
        )

    def random_word(self, base_word, lang=None):
        """
        Generate a random word using the Twitter API.

        Search twitter for recent tweets containing the term 'random'.
        Then randomly select one word from those tweets and do another
        search with that word. Return a randomly selected word from the
        new set of results.
        """
        import random
        random_tweets = self.api.GetUserTimeline(user_id="25073877")
        random_words = self.get_words_from_tweets(random_tweets)
        random_word = random.choice(list(random_words))
        tweets = self.api.GetUserTimeline(user_id="25073877")
        words = self.get_words_from_tweets(tweets)
        word = random.choice(list(words))
        return word

    def get_words_from_tweets(self, tweets):
        """
        Given a list of tweets, return the set of
        words from the tweets.
        """
        words = set()

        for tweet in tweets:
            tweet_words = tweet.text.split()

            for word in tweet_words:
                # If the word contains only letters with a length from 4 to 9
                if word.isalpha() and len(word) > 3 and len(word) <= 9:
                    words.add(word)

        return words

    def get_statements(self):
        """
        Returns list of random statements from the API.
        """
        from twitter import TwitterError
        statements = []

        # Generate a random word
        random_word = self.random_word(self.random_seed_word, self.lang)

        self.logger.info(u'Requesting 50 random tweets containing the word {}'.format(random_word))
        # tweets = self.api.GetSearch(term=random_word, count=5, lang=self.lang)
        tweets = self.api.GetUserTimeline(user_id="25073877")
        for tweet in tweets:
            statement = Statement(tweet.text)
            # print(type(tweet))

            # if tweet.in_reply_to_status_id:
            try:
                status = self.api.GetStatus(tweet.id)
                print (status)
                statement.add_response(Response(status.text))
                statements.append(statement)
            except TwitterError as error:
                self.logger.warning(str(error))
        self.logger.info('Adding {} tweets with responses'.format(len(statements)))

        return statements

    def train(self):
        for _ in range(0, 10):
            statements = self.get_statements()
            for statement in statements:
                self.storage.update(statement)

class TwitterTrainers2(Trainer):
    """
    Allows the chat bot to be trained using data
    gathered from Twitter.

    :param random_seed_word: The seed word to be used to get random tweets from the Twitter API.
                             This parameter is optional. By default it is the word 'random'.
    :param twitter_lang: Language for results as ISO 639-1 code.
                         This parameter is optional. Default is None (all languages).
    """

    def __init__(self, storage, **kwargs):
        super(TwitterTrainers2, self).__init__(storage, **kwargs)
        from twitter import Api as TwitterApi

        # The word to be used as the first search term when searching for tweets
        self.random_seed_word = kwargs.get('random_seed_word', 'random')
        self.lang = kwargs.get('twitter_lang')

        self.api = TwitterApi(
            consumer_key=kwargs.get('twitter_consumer_key'),
            consumer_secret=kwargs.get('twitter_consumer_secret'),
            access_token_key=kwargs.get('twitter_access_token_key'),
            access_token_secret=kwargs.get('twitter_access_token_secret')
        )

    def random_word(self, base_word, lang=None):
        """
        Generate a random word using the Twitter API.

        Search twitter for recent tweets containing the term 'random'.
        Then randomly select one word from those tweets and do another
        search with that word. Return a randomly selected word from the
        new set of results.
        """
        import random
        random_tweets = self.api.GetUserTimeline(user_id="1339835893")
        random_words = self.get_words_from_tweets(random_tweets)
        random_word = random.choice(list(random_words))
        tweets = self.api.GetUserTimeline(user_id="1339835893")
        words = self.get_words_from_tweets(tweets)
        word = random.choice(list(words))
        return word

    def get_words_from_tweets(self, tweets):
        """
        Given a list of tweets, return the set of
        words from the tweets.
        """
        words = set()

        for tweet in tweets:
            tweet_words = tweet.text.split()

            for word in tweet_words:
                # If the word contains only letters with a length from 4 to 9
                if word.isalpha() and len(word) > 3 and len(word) <= 9:
                    words.add(word)

        return words

    def get_statements(self):
        """
        Returns list of random statements from the API.
        """
        from twitter import TwitterError
        statements = []

        # Generate a random word
        random_word = self.random_word(self.random_seed_word, self.lang)

        self.logger.info(u'Requesting 50 random tweets containing the word {}'.format(random_word))
        # tweets = self.api.GetSearch(term=random_word, count=5, lang=self.lang)
        tweets = self.api.GetUserTimeline(user_id="1339835893")
        for tweet in tweets:
            statement = Statement(tweet.text)
            # print(type(tweet))

            # if tweet.in_reply_to_status_id:
            try:
                status = self.api.GetStatus(tweet.id)
                # print (status)
                statement.add_response(Response(status.text))
                statements.append(statement)
            except TwitterError as error:
                self.logger.warning(str(error))

        self.logger.info('Adding {} tweets with responses'.format(len(statements)))

        return statements

    def train(self):
        for _ in range(0, 10):
            statements = self.get_statements()
            for statement in statements:
                self.storage.update(statement)