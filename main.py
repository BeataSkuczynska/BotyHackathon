from chatterbot import ChatBot
from settings import TWITTER
import logging


'''
This example demonstrates how you can train your chat bot
using data from Twitter.

To use this example, create a new file called settings.py.
In settings.py define the following:

TWITTER = {
    "CONSUMER_KEY": "my-twitter-consumer-key",
    "CONSUMER_SECRET": "my-twitter-consumer-secret",
    "ACCESS_TOKEN": "my-access-token",
    "ACCESS_TOKEN_SECRET": "my-access-token-secret"
}
'''


if __name__ == "__main__":

    # Comment out the following line to disable verbose logging
    logging.basicConfig(level=logging.INFO)

    hillary = ChatBot(
        "HillaryBot",
        logic_adapters=[
            {'import_path': 'test_chatterbot.MyLogicAdapter'},
        ],
        input_adapter="chatterbot.input.TerminalAdapter",
        output_adapter="chatterbot.output.TerminalAdapter",
        database="./hillary-database.db",
        twitter_consumer_key=TWITTER["CONSUMER_KEY"],
        twitter_consumer_secret=TWITTER["CONSUMER_SECRET"],
        twitter_access_token_key=TWITTER["ACCESS_TOKEN"],
        twitter_access_token_secret=TWITTER["ACCESS_TOKEN_SECRET"],
        trainer="chatterbot.trainers.TwitterTrainer",
    )

    donald = ChatBot(
        "DonaldBot",
        logic_adapters=[
            {'import_path': 'test_chatterbot.MyLogicAdapter'},
        ],
        input_adapter="chatterbot.input.TerminalAdapter",
        output_adapter="chatterbot.output.TerminalAdapter",
        database="./donald-database.db",
        twitter_consumer_key=TWITTER["CONSUMER_KEY"],
        twitter_consumer_secret=TWITTER["CONSUMER_SECRET"],
        twitter_access_token_key=TWITTER["ACCESS_TOKEN"],
        twitter_access_token_secret=TWITTER["ACCESS_TOKEN_SECRET"],
        trainer="chatterbot.trainers.TwitterTrainer",
    )

    # for i in range(3):
    #     hillary.train()
    #     donald.train()

    hillary.logger.info('Trained Hillary generated successfully!')
    donald.logger.info('Trained Donald generated successfully!')
    # print(chatbot.storage.find("dumb"))


    while True:
        try:
            bot = hillary.get_response(None)
            bots = donald.get_response(None)
        except(KeyboardInterrupt, EOFError, SystemExit):
            break