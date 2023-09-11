import time
from chatbot_lib import ChatBot
chatbot = ChatBot(config_file="config.json")

# Start a conversation
response = chatbot.chatbot_conversation("我跟我男朋友分手")
print(response)
print(chatbot._is_ending)
time.sleep(30)

# Continue the conversation
response = chatbot.chatbot_conversation("我和我男朋友分手了，因为我们的性格不合，经常吵架")
print(response)
print(chatbot._is_ending)
time.sleep(30)

# Continue the conversation
response = chatbot.chatbot_conversation("感觉很抱歉听到我们分手的消息，分手是很困难的事情")
print(response)
print(chatbot._is_ending)
time.sleep(30)

# Continue the conversation
response = chatbot.chatbot_conversation("现在我希望能够好好照顾自己，倾听自己的内心和感受")
print(response)
print(chatbot._is_ending)
time.sleep(30)

# Continue the conversation
response = chatbot.chatbot_conversation("我知道分手可能是因为我们性格不合和经常吵架的原因")
print(response)
print(chatbot._is_ending)
time.sleep(30)

# Continue the conversation
response = chatbot.chatbot_conversation("有时候，人们会发现自己和伴侣的价值观、兴趣爱好或者生活方式不一致，这可能导致无法和谐相处")
print(response)
print(chatbot._is_ending)
time.sleep(30)

# Continue the conversation
response = chatbot.chatbot_conversation("但是，分手也可以是一个新的开始，让每个人都能够在寻找适合自己的伴侣和幸福的道路上继续前进")
print(response)
print(chatbot._is_ending)
time.sleep(30)

# Continue the conversation
response = chatbot.chatbot_conversation("无论如何，我需要给自己一些时间来愈合和恢复，关注自己的需求和内心的感受")
print(response)
print(chatbot._is_ending)
time.sleep(30)

# Continue the conversation
response = chatbot.chatbot_conversation("没有")
print(response)
print(chatbot._is_ending)
time.sleep(30)

# Generate a summary of the conversation
print("===== Summary =======")
summary = chatbot.chatbot_summary()
print(summary)
time.sleep(60)

# Generate a title for summary of the conversation
print("======= Title =======")
title = chatbot.generate_tittle()
print(title)
time.sleep(60)

# Generate 3 questions that user would like to ask the coach
print("======= Question =======")
questions = chatbot.generate_questions()
print(questions)
time.sleep(60)

# Generate the category for the conversation
print("======= Category =====")
category = chatbot.get_category()
print(category)
time.sleep(60)

# Generate the most 3 related tags
tags = chatbot.get_tags()
print(tags)