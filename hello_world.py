from chatterbot import ChatBot
from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement
from settings import TWITTER
import logging
import sys
import re

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
trump=[]
hillary=[]
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

    def getTable(self):
        return trump

    def process(self, statement):
        # import pdb
        # pdb.set_trace()
        trimmed = re.sub(r'[^\w\s]',' ',statement.text).split()
        statements = []
        for trim in trimmed:
            for sentence in self.getTable():
                if trim.lower() in sentence.lower():
                    statements.append(Statement(sentence))
        for stat in statements:
            stat.text = re.sub('@\\w+', ' ', stat.text)
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

class HillaryLogicAdapter(MyLogicAdapter):
    def getTable(self):
        return hillary


trumpBot = ChatBot(
    "trumpBot",
    logic_adapters = [{'import_path': 'hello_world.MyLogicAdapter'}],
    filters=["chatterbot.filters.RepetitiveResponseFilter"],
    database="./twitter-database.db",
    twitter_consumer_key=TWITTER["CONSUMER_KEY"],
    twitter_consumer_secret=TWITTER["CONSUMER_SECRET"],
    twitter_access_token_key=TWITTER["ACCESS_TOKEN"],
    twitter_access_token_secret=TWITTER["ACCESS_TOKEN_SECRET"]
)
hillaryBot = ChatBot(
    "trumpBot",
    logic_adapters = [{'import_path': 'hello_world.HillaryLogicAdapter'}],
    filters=["chatterbot.filters.RepetitiveResponseFilter"],
    database="./twitter-database.db",
    twitter_consumer_key=TWITTER["CONSUMER_KEY"],
    twitter_consumer_secret=TWITTER["CONSUMER_SECRET"],
    twitter_access_token_key=TWITTER["ACCESS_TOKEN"],
    twitter_access_token_secret=TWITTER["ACCESS_TOKEN_SECRET"]
)
with open("trump.txt") as trump_data:
    for line in trump_data:
        trump.append(line)

with open("hillary.txt") as trump_data:
    for line in trump_data:
        hillary.append(line)

while True:
    try:
        v = input("Me: ")
        print("Donald Trump: "+str(trumpBot.get_response(v)))
        print("Hillary Clinton: "+str(hillaryBot.get_response(v)))

    except(KeyboardInterrupt, EOFError, SystemExit):
        pass