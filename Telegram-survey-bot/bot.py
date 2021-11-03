import requests 
import configparser as cp
import json 

# BOT class to communicate with API
# most of the methods are self explanatory

class Bot:
    def __init__(self, config):
        self.token = self.get_token(config)
        self.base = r"https://api.telegram.org/bot{}/".format(self.token)
    
    def get_token(self, config):
        parser = cp.ConfigParser()
        parser.read(config)
        return parser.get("credentials","token")
    
    def get_updates(self, offset = None):
        url = self.base + "getupdates"
        params = {"timeout":100, "allowed_upates":[]}
        
        if offset:
            params.update({"offset":offset+1})
        
        request = requests.get(url, params=params)
        return request.json()
    
    def send_message(self, chat_id, message, ReplyKeyboardMarkup = None, InlineKeyboardMarkup = None):
        url = self.base + "sendmessage"
        params = {"chat_id": chat_id}
        
        if message:
            params.update({"text": message})
        if InlineKeyboardMarkup:
            params.update({"reply_markup": InlineKeyboardMarkup})
        if ReplyKeyboardMarkup:
            params.update({"reply_markup": ReplyKeyboardMarkup})
    
        req = requests.get(url, params=params)
        return req

    def answer_callback_query(self, callback_query_id):
        url = self.base + "answerCallbackQuery"
        params = {"callback_query_id": callback_query_id, "text":""}
        req = requests.get(url, params=params)
        return req

    def get_custom_keyboard(self, choices, one_time = True, resize = True):
        reply_markup = {"keyboard": choices,"resize_keyboard": resize,"one_time_keyboard": one_time}
        reply_markup = json.dumps(reply_markup)
        return reply_markup

    def get_inline_keyboard(self, choices):
        reply_markup = {"inline_keyboard": [[choice] for choice in choices]}
        reply_markup = json.dumps(reply_markup)
        return reply_markup
    
    def edit_message_text(self, chat_id, message_id, message, reply_markup):
        url = self.base + "editmessagetext"
        params = {"chat_id":chat_id, "message_id":message_id, "text":message, "reply_markup":reply_markup}
        return requests.get(url, params=params)