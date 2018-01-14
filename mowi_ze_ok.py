from chatterbot import ChatBot
from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement
from settings import TWITTER
import logging
import sys
import re
from TwitterTrainer2 import TwitterTrainers

TRIGGERS={"Donald":1.04, "Trump":1.03,
                "America":1.02,
                "Hillary":1.01,
                "Clinton":1,
                "president":0.91,
                "job":0.9,
                "islam":0.81,
                "isis":0.8,
                "media":0.72,
                "obama":0.71,
                "mexico":0.7,
                "mexicans":0.7,
                "nuclear":0.63,
                "Iraq":0.62,
                "Putin":0.6,
                "African_american":0.56,
                "middle class":0.55,
                "police":0.54,
                "e-mail":0.53,
                "email":0.52,
                "tax,":0.51,
          }
used=[]
class MyLogicAdapter(LogicAdapter):


    def __init__(self, **kwargs):
        super(MyLogicAdapter, self).__init__(**kwargs)

    def can_process(self, statement):
        return True

    def find_best(self, statements):
        best_statement=statements[0]
        best_value=0
        for statement in statements:
            if statement.text in used:
                continue
            value=0
            for w, n in TRIGGERS.items():
                if w in statement.text:
                    value=value+n
            if value > best_value:
                best_value=value
                best_statement=statement
            best_statement.value=best_value/30
        return best_statement


    def process(self, statement):
        # import pdb
        # pdb.set_trace()
        trimmed = re.sub(r'[^\w\s]',' ',statement.text).split()
        statements = []
        for trim in trimmed:
            [statements.append(v) for v in self.chatbot.storage.filter(text=trim) if v is not statement]
            # pdb.set_trace()
        for stat in statements:
            stat.text = re.sub('@\\w+', ' ', stat.text)
        # pdb.set_trace()
        if len(statements) == 0:
            statement.confidence = 0
            statement.text = "I know nothing about that!"
            return statement

        retStat = self.find_best(statements)
        used.append(retStat.text)
        retStat.confidence=1
        if statement is retStat:
            statement.text="I know nothing about that!"
            statement.confidence = 0
            return statement
        return retStat


donald = ChatBot(
    "DonaldBot",
    logic_adapters = [{'import_path': 'mowi_ze_ok.MyLogicAdapter'}],
    filters=["chatterbot.filters.RepetitiveResponseFilter"],
    database="./donald-database.db",
    twitter_consumer_key=TWITTER["CONSUMER_KEY"],
    twitter_consumer_secret=TWITTER["CONSUMER_SECRET"],
    twitter_access_token_key=TWITTER["ACCESS_TOKEN"],
    twitter_access_token_secret=TWITTER["ACCESS_TOKEN_SECRET"],
    trainer="TwitterTrainer2.TwitterTrainers"
)
hillary = ChatBot(
    "HillaryBot",
    logic_adapters = [{'import_path': 'mowi_ze_ok.MyLogicAdapter'}],
    filters=["chatterbot.filters.RepetitiveResponseFilter"],
    database="./hillary-database.db",
    twitter_consumer_key=TWITTER["CONSUMER_KEY"],
    twitter_consumer_secret=TWITTER["CONSUMER_SECRET"],
    twitter_access_token_key=TWITTER["ACCESS_TOKEN"],
    twitter_access_token_secret=TWITTER["ACCESS_TOKEN_SECRET"],
    trainer="TwitterTrainer2.TwitterTrainers2"
)

# for i in range(3):
donald.train()
    # hillary.train()

# hillary.logger.info('Trained Hillary generated successfully!')
donald.logger.info('Trained Donald generated successfully!')

while True:
    try:
        v = input()
        print(donald.get_response(v))
        # print(hillary.get_response(v))

    except(KeyboardInterrupt, EOFError, SystemExit):
        pass# your code goes here