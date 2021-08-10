# clear the already existing data by running this file
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer
import csv
data = open("dataset.csv")
print("Hi, I'm the AgroXpert,Have doubts on farming?I am here to help you\n")
# creating a new chatbot
chatbot = ChatBot(name='AgroXpert', read_only=True,
                  logic_adapters=[
                                  {"import_path": "chatterbot.logic.BestMatch",
                                      "statement_comparision_function": "chatterbot.comparisions.levenshtein_distance",
                                    'maximum_similarity_threshold': 0.55
                                   }])
chatbot.storage.drop()
trainer = ListTrainer(chatbot)
for item in csv.reader(data):
    trainer.train(item)
print("What is your query:")
chatbot.storage.create_many([
    Statement('Example A for search.'),
    Statement('Another example.'),
    Statement('Example B for search.'),
    Statement(text='Another statement.'),
])

results = list(chatbot.storage.filter(
    search_text=chatbot.storage.tagger.get_bigram_pair_string(
        'Example A for search.'
    )
))

while (True):
    qns = input()
    """    if qns=="quit" or qns=="Quit" or qns=="Thanks":
      response = chatbot.get_response(qns)
      print(response)
      break"""
    response = chatbot.get_response(qns)
    print(response)