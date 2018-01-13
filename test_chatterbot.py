from chatterbot import ChatBot
import logging


from chatterbot.logic import LogicAdapter


class MyLogicAdapter(LogicAdapter):
    def __init__(self, **kwargs):
        super(MyLogicAdapter, self).__init__(**kwargs)

    def can_process(self, statement):
        return True

    def process(self, statement):

        statements = self.chatbot.storage.filter(text=statement.text)
        if len(statements) == 0:
            statement.confidence = 0
            return statement

        statement = statements[0]

        response_list = self.chatbot.storage.filter(
                        in_response_to__contains=statement.text
        )
        if len(response_list) == 0:
            statement.confidence = 0
            return statement

        response = response_list[0]
        response.confidence = 1.0

        return response


if __name__ == "__main__":

    # Enable info level logging
    logging.basicConfig(level=logging.INFO)

    chatbot = ChatBot(
        'Example Bot',
        trainer='chatterbot.trainers.ChatterBotCorpusTrainer',
        logic_adapters = [{'import_path': 'test_chatterbot.MyLogicAdapter'}]
    )

    # Start by training our bot with the ChatterBot corpus data
    chatbot.train(
        'chatterbot.corpus.english.greetings'
    )


    # Now let's get a response to a greeting
    response = chatbot.get_response('How are you')
    print(response)
