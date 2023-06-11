import openai
import json
import os
from dotenv import load_dotenv
import time

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

LAST_CALL_TIME = 0

class ChatBot:
    def __init__(self, config_file=None, chat_history=None):
        if config_file is not None:
            with open(config_file) as f:
                config = json.load(f)
        else:
            config = {
                        "initial_message": {
                            "role": "system",
                            "content": "You are ChatBot, an empathetic assistant of professional mental counselor in a mental counseling session. You will talk with client who is seeking mental help. You first greet the client. Then please ask client 25 empathy curious deep open-ended questions to get more specific information as much as possible about the problem of client to find out the cause of problem. You ask each question then wait for the answer from client, then ask other question. Please to not provide any advice or suggestion to client. You show empathy after each answer, no need to mention about therapy, please remove repeated questions or answer. The purpose of this conversation is to gather client information so that the real therapist can provide suggestion, the conversation start from you saying thanks for coming and ask what brings them to counseling. Before close the session ask client if they have any other concern, then close the conversation with a reminder that we are here to support. Finish with \"Goodbye!\""
                        },
                        "summary_prompt": {
                            "content": "Your task is to generate a short summary about client mental issue from a conversation in a counselling session.\n\nSummarize the conversation below, delimited by triple backticks, in at most 250 words."
                        },
                        "rate_limit": 20,
                        "model_engine": "gpt-3.5-turbo"
                    }
        self._initial_message   = config.get("initial_message", {}).get("content", "Hello, how can I help you?")
        self._rate_limit        = int(config.get("rate_limit", 20))
        self._summary_prompt    = config.get("summary_prompt", {}).get("content", "Can you summarize our conversation?")
        self._model_engine      = config.get("model_engine", "gpt-3.5-turbo")

        if chat_history is None:
            self._chat_history = {"messages": [{"role": "system", "content": self._initial_message}]}
        else:
            self._chat_history = chat_history

    def generate_response(self, messages):
        try:
            chat = openai.ChatCompletion.create(model=self._model_engine, messages=messages)
            return chat.choices[0].message.content
        except Exception as e:
            raise Exception(f"Failed to generate bot response: {e}")

    def _check_rate_limit(self):
        global LAST_CALL_TIME
        current_time = time.time()
        if current_time - LAST_CALL_TIME < self._rate_limit:
            raise Exception("Rate limit exceeded. Please wait a few seconds before trying again.")
        LAST_CALL_TIME = current_time

    def chatbot_conversation(self, user_input):
        self._check_rate_limit()

        current_message = {"role": "user", "content": user_input}
        self._chat_history["messages"].append(current_message) 

        try:
            bot_response = self.generate_response(self._chat_history["messages"])
        except Exception as e:
            raise Exception(f"Failed to get bot response: {e}")
        self._chat_history["messages"].append({"role": "assistant", "content": bot_response})

        return bot_response

    def chatbot_summary(self):
        self._check_rate_limit()

        chat_log = self._chat_history["messages"]
        prompt = f"{self._summary_prompt}\n\nConversation: ```{chat_log}```"
        summary_request = [{"role": "user", "content": prompt}]
        
        try:
            summary = self.generate_response(summary_request)
        except Exception as e:
            raise Exception(f"Failed to get bot response: {e}")
            
        return summary