import time
from chatbot_lib import ChatBot
chatbot = ChatBot(config_file="config.json")

# Start a conversation
response = chatbot.chatbot_conversation("我跟我男朋友分手")
print(response)
time.sleep(30)

# Continue the conversation
response = chatbot.chatbot_conversation("我們性格不合, 經常吵架")
print(response)
time.sleep(30)

# Generate a summary of the conversation
summary = chatbot.chatbot_summary()
print(summary)
time.sleep(60)

# Generate a title for summary of the conversation
title = chatbot.generate_tittle()
print(title)
time.sleep(60)

# Generate 3 questions that user would like to ask the coach
questions = chatbot.generate_questions()
print(questions)
time.sleep(60)

# Generate the category for the conversation
category = chatbot.get_category()
print(category)
time.sleep(60)

# Generate the most 3 related tags
tags = chatbot.get_tags()
print(tags)