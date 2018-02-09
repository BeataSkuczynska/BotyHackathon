from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement
import re
from settings import TRIGGERS, DONALD_CORPUS, HILLARY_CORPUS


USED = []


class DonaldLogicAdapter(LogicAdapter):

    def __init__(self, **kwargs):
        super(DonaldLogicAdapter, self).__init__(**kwargs)

    def can_process(self, statement):
        return True

    @staticmethod
    def find_best(statements):
        best_statement = statements[0]
        best_value = 0
        for statement in statements:
            if statement.text in USED:
                continue
            value = 0
            for word, weight in TRIGGERS.items():
                if word in statement.text:
                    value += weight
            if value > best_value:
                best_value = value
                best_statement = statement
            best_statement.value = best_value/30
        return best_statement

    def get_table(self):
        donald = []
        with open(DONALD_CORPUS, encoding='utf-8') as file:
            try:
                for line in file:
                    donald.append(line)
            except UnicodeDecodeError:
                pass
        return donald

    def process(self, statement):
        trimmed = re.sub(r'[^\w\s]', ' ', statement.text).split()
        statements = []
        for trim in trimmed:
            for sentence in self.get_table():
                if trim.lower() in sentence.lower():
                    statements.append(Statement(sentence))
        for stat in statements:
            stat.text = re.sub('@\\w+', ' ', stat.text)
        if len(statements) == 0:
            statement.confidence = 0
            statement.text = "I know nothing about that!"
            return statement

        ret_stat = self.find_best(statements)
        USED.append(ret_stat.text)
        ret_stat.confidence = 1
        if statement is ret_stat:
            statement.text = "I know nothing about that!"
            statement.confidence = 0
            return statement
        return ret_stat


class HillaryLogicAdapter(DonaldLogicAdapter):

    def get_table(self):
        hillary = []
        with open(HILLARY_CORPUS, encoding='utf-8') as file:
            try:
                for line in file:
                    hillary.append(line)
            except UnicodeDecodeError:
                pass

        return hillary
