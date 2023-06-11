import time
from chatbot_lib import ChatBot
chatbot = ChatBot()

# Start a conversation
response = chatbot.chatbot_conversation("Hi there!")
print(response)
time.sleep(30)

# Continue the conversation
response = chatbot.chatbot_conversation("I'm feeling really anxious today.")
print(response)
time.sleep(30)
# Generate a summary of the conversation
summary = chatbot.chatbot_summary()
print(summary)
