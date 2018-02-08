from chatterbot import ChatBot
from settings import TWITTER


donald_bot = ChatBot(
    "Donald Bot",
    logic_adapters=[{'import_path': 'logic_adapters.DonaldLogicAdapter'}],
    filters=["chatterbot.filters.RepetitiveResponseFilter"],
    twitter_consumer_key=TWITTER["CONSUMER_KEY"],
    twitter_consumer_secret=TWITTER["CONSUMER_SECRET"],
    twitter_access_token_key=TWITTER["ACCESS_TOKEN"],
    twitter_access_token_secret=TWITTER["ACCESS_TOKEN_SECRET"]
)

hillary_bot = ChatBot(
    "Hillary Bot",
    logic_adapters=[{'import_path': 'logic_adapters.HillaryLogicAdapter'}],
    filters=["chatterbot.filters.RepetitiveResponseFilter"],
    twitter_consumer_key=TWITTER["CONSUMER_KEY"],
    twitter_consumer_secret=TWITTER["CONSUMER_SECRET"],
    twitter_access_token_key=TWITTER["ACCESS_TOKEN"],
    twitter_access_token_secret=TWITTER["ACCESS_TOKEN_SECRET"]
)

if __name__ == '__main__':
    while True:
        try:
            terminal_input = input("Me: ")
            print("Donald Trump: " + str(donald_bot.get_response(terminal_input)))
            print("Hillary Clinton: " + str(hillary_bot.get_response(terminal_input)))
        except(KeyboardInterrupt, EOFError, SystemExit):
            pass
