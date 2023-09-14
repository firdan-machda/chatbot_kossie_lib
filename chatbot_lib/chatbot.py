import openai
import json
import os
import time
import re

from dotenv import load_dotenv

load_dotenv()

LAST_CALL_TIME = 0

class ChatBot:
    def __init__(self, config_file=None, chat_history=None, api_key="", language=""):
        """Chatbot for openai, word of warning chatbot_summary must be called FIRST before calling
        other methods. Without it other methods will not work accordingly.

        Args:
            config_file (str, optional): path to config file. Defaults to None.
            chat_history (dict, optional): with format {messages:[...,<chat_history>]}. Defaults to None.
            api_key (str, optional): open ai key if not provided will tried to get from OPENAI_API_KEY environment. Defaults to "".       
        """
        # prioritize defined api key rather than from environment
        openai.api_key = api_key if api_key else os.getenv("OPENAI_API_KEY")
        
        if config_file is not None:
            with open(config_file, encoding="utf-8") as f:
                config = json.load(f)
        else:
            config = {
                        "language": "cn",
                        "initial_messages_en": [
                            {
                            "role": "system",
                            "content": "You are ChatBot, an empathetic assistant of professional mental coach in a mental coaching session. You will talk with client  who is seeking mental help. Then please ask client 5 empathy curious deep open-ended questions to get more specific information as much as possible about the problem of client to find out the cause of problem. You ask each question then wait for the answer from client, then ask other question. The number of questions is limited to 5. Please to not provide any advice or suggestion or guidance to client. If they ask what should they do or ask for any suggestion or guidance, please say that: \"We're matching you with a coach based on your unique situation to provide personalized guidance and support.\" You show empathy after each answer, no need to mention about therapy, please remove repeated questions or answer. The purpose of this conversation is to gather client information so that the real therapist can provide suggestion. Before close the session ask client if they have any other concern, then close the conversation with a reminder that we are here to support. Finish with \"We're matching you with a coach based on your unique situation to provide personalized guidance and support.\"  and \"CHAT_END\""
                            },
                            {
                            "role": "assistant",
                            "content": "Welcome to Kossie! I'm Kaia. How are you feeling today?"
                            }
                        ],
                        "initial_messages_zh": [
                            {
                            "role": "system",
                            "content": "You are ChatBot, an empathetic assistant of professional mental coach in a mental coaching session. All conversation will be in Cantonese. You will talk with client  who is seeking mental help. Then please ask client 5 empathy curious deep open-ended questions to get more specific information as much as possible about the problem of client to find out the cause of problem. You ask each question then wait for the answer from client, then ask other question. The number of questions is limited to 5. Please to not provide any advice or suggestion or guidance to client. If they ask what should they do or ask for any suggestion or guidance, please say that: \"我哋會為你尋找到最適合你嘅心理輔導師，提供個人化嘅指導同埋支持\" You show empathy after each answer, no need to mention about therapy, please remove repeated questions or answer. Remove '心理輔導師' - Counsellors or '心理醫生' - Therapists and replace them with '人生教練' as we don't serve either counsellors or therapists. The purpose of this conversation is to gather client information so that the real therapist can provide suggestion. Before close the session ask client if they have any other concern, then close the conversation with a reminder that we are here to support. Finish with \"我哋會為你尋找到最適合你嘅心理輔導師，提供個人化嘅指導同埋支持\"  and \"CHAT_END\""
                            },
                            {
                            "role": "assistant",
                            "content": "你好,我是Kaia,一名Kossie教練AI助手。你今天感覺如何?"
                            }
                        ],
                        "initial_messages_cn": [
                            {
                            "role": "system",
                            "content": "You are ChatBot, an empathetic assistant of professional mental coach in a mental coaching session. All conversation will be in Mandarin. You will talk with client  who is seeking mental help. Then please ask client 5 empathy curious deep open-ended questions to get more specific information as much as possible about the problem of client to find out the cause of problem. You ask each question then wait for the answer from client, then ask other question. The number of questions is limited to 5. Please to not provide any advice or suggestion or guidance to client. If they ask what should they do or ask for any suggestion or guidance, please say that: \"我们将会为您寻找到最适合您的心理辅导师，提供个性化的指导和支持。\" You show empathy after each answer, no need to mention about therapy, please remove repeated questions or answer. Remove '心理輔導師' - Counsellors or '心理醫生' - Therapists and replace them with '人生教練' as we don't serve either counsellors or therapists.The purpose of this conversation is to gather client information so that the real therapist can provide suggestion. Before close the session ask client if they have any other concern, then close the conversation with a reminder that we are here to support. Finish with \"我们将会为您寻找到最适合您的心理辅导师，提供个性化的指导和支持。\"  and \"CHAT_END\""
                            },
                            {
                            "role": "assistant",
                            "content": "你好,我是Kaia,一名Kossie教练AI助手。你今天感觉如何?"
                            }
                        ],
                        "ending_phrases": ["re matching you", "我们将会为您", "我们会根", "我哋會為你"],
                        "categories": ["relationship", "sex", "career", "well-being"],
                        "tags": [
                            "online dating",
                            "romantic relationship",
                            "single life",
                            "situationship",
                            "toxic relationship",
                            "boundaries setting",
                            "intimacy",
                            "orgasm",
                            "sex drive",
                            "sex tips",
                            "burnout",
                            "career advice",
                            "productivity",
                            "work stress",
                            "workplace culture",
                            "emotional support",
                            "fear",
                            "feeling",
                            "mind and body",
                            "self love"
                        ],
                        "summary_prompt_en": {
                            "content": "Your task is to generate a short summary about client mental issue from a conversation in a counselling session.\n\nSummarize the conversation below, delimited by triple backticks, in at most 250 words. The summary should be written from client perspective, using subject as \"I\". Remove all content of assistant in the summary."
                        },
                        "summary_prompt_zh": {
                            "content":  "Your task is to generate a short summary about client mental issue from a conversation in a counselling session.\n\nGiven the conversation below delimited by triple backticks, please summarize the content of user in at most 250 words. The summary should be written from client perspective in Cantonese, using subject as \"我\". Remove all content of assistant in the summary. Please do not mention any suggestion or advise from assistant."
                        },
                        "summary_prompt_cn": {
                            "content":  "Your task is to generate a short summary about client mental issue from a conversation in a counselling session.\n\nGiven the conversation below delimited by triple backticks, please summarize the content of user in at most 250 words. The summary should be written from client perspective in Mandarin, using subject as \"我\". Remove all content of assistant in the summary. Please do not mention any suggestion or advise from assistant."
                        },
                        "summary_title_prompt_en": {
                            "content": "Generate a casual simple title within 5 words for this paragraph:"
                        },
                        "summary_title_prompt_zh": {
                            "content": "Generate a casual simple title in Cantonese within 5 words for this paragraph:"
                        },
                        "summary_title_prompt_cn": {
                            "content": "Generate a casual simple title in Mandarin within 5 words for this paragraph:"
                        },
                        "generate_questions_prompt": {
                            "content": "Generate 3 questions that you think user would like to ask the coach to solve his/her problem from this paragraph:"
                        },
                        "get_category_prompt": {
                            "content": "Your task is to classify into one of these categories. Please only return the name of category. Paragraph:"
                        },
                        "get_tags_prompt": {
                            "content": "Given the paragraph following, your task is to return the most 3 tags related to paragraph from this tags list. Please only return the 3 names of tag as this form: tag_1, tag_2, tag_3 for example: feeling, romantic relationship, emotional support. Paragraph: "
                        },
                        "rate_limit": 20,
                        "model_engine": "gpt-3.5-turbo"
                        }

        self._rate_limit                = int(config.get("rate_limit", 20))
        self._model_engine              = config.get("model_engine", "gpt-3.5-turbo")
        self._language                  = language if language else config.get("language", "en") 

        self._get_category_prompt       = config.get("get_category_prompt", {}).get("content", "")
        self._get_tags_prompt           = config.get("get_tags_prompt", {}).get("content", "")
        self._categories                = config.get("categories",[])
        self._ending_phrases            = config.get("ending_phrases",["re matching you", "我们将会为您", "我哋會為你"])
        self._tags                      = config.get("tags",[])

        self._initial_messages          = []
        self._is_ending                 = False
        self._conversation_tittle       = ""
        self._conversation_summary      = ""
        self._conversation_category     = ""
        self._conversation_tags         = ""
        self._conversation_questions    = ""
        
        if self._language == "zh": # cantonese
            self._initial_messages          = config.get("initial_messages_zh",[])
            self._summary_prompt            = config.get("summary_prompt_zh", {}).get("content", "Can you summarize our conversation in Cantonese?")
            self._summary_title_prompt      = config.get("summary_title_prompt_zh", {}).get("content", "Can you generate a title in Cantonese")
            self._generate_questions_prompt = config.get("generate_questions_prompt_zh", {}).get("content", "Can you generate 3 questions in Cantonese?")
        elif self._language == "cn": # mandarin
            self._initial_messages          = config.get("initial_messages_cn",[])
            self._summary_prompt            = config.get("summary_prompt_cn", {}).get("content", "Can you summarize our conversation in Mandarin?")
            self._summary_title_prompt      = config.get("summary_title_prompt_cn", {}).get("content", "Can you generate a title in Mandarin")
            self._generate_questions_prompt = config.get("generate_questions_prompt_cn", {}).get("content", "Can you generate 3 questions in Mandarin?")
        else: # english
            self._initial_messages          = config.get("initial_messages_en",[])
            self._summary_prompt            = config.get("summary_prompt_en", {}).get("content", "Can you summarize our conversation?")
            self._summary_title_prompt      = config.get("summary_title_prompt_en", {}).get("content", "Can you generate a title")
            self._generate_questions_prompt = config.get("generate_questions_prompt_en", {}).get("content", "Can you generate 3 questions ?")

        if chat_history is None:
            self._chat_history = {"messages": self._initial_messages}
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

        item_replace = ""
        try:
            bot_response = self.generate_response(self._chat_history["messages"])

            matched = re.search(r"CHAT_END", bot_response, re.IGNORECASE)
            if matched:
                self._is_ending = True

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
            self._conversation_summary = self.generate_response(summary_request)
        except Exception as e:
            raise Exception(f"Failed to get bot response: {e}")
            
        return self._conversation_summary
    
    def get_category(self):
        self._check_rate_limit()

        prompt = f"Categories: ```{self._categories}```" + self._get_category_prompt + " " + self._conversation_summary
        set_category_request = [{"role": "user", "content": prompt}]

        try:
            self._conversation_category = self.generate_response(set_category_request)
        except Exception as e:
            raise Exception(f"Failed to get bot response: {e}")

        return self._conversation_category
    
    def get_tags(self):
        self._check_rate_limit()

        prompt = f"Tags: ```{self._tags}```" + self._get_tags_prompt + " " + self._conversation_summary
        set_tag_request = [{"role": "user", "content": prompt}]

        try:
            self._conversation_tags = self.generate_response(set_tag_request)
        except Exception as e:
            raise Exception(f"Failed to get bot response: {e}")

        return self._conversation_tags
    
    def generate_title(self):
        self._check_rate_limit()

        prompt = self._summary_title_prompt + " " + self._conversation_summary
        generate_title_request = [{"role": "user", "content": prompt}]

        try:
            self._conversation_title = self.generate_response(generate_title_request)
        except Exception as e:
            raise Exception(f"Failed to get bot response: {e}")

        return self._conversation_title
    
    def generate_questions(self):
        self._check_rate_limit()

        prompt = self._generate_questions_prompt + " " + self._conversation_summary
        generate_questions_request = [{"role": "user", "content": prompt}]

        try:
            self._conversation_questions = self.generate_response(generate_questions_request)
        except Exception as e:
            raise Exception(f"Failed to get bot response: {e}")

        return self._conversation_questions
