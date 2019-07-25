from flask import Flask, request, abort
import requests
import re
import random
import configparser
import urllib3
from bs4 import BeautifulSoup
from initialization import Initialization

'''import linebot sdk'''
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)

from linebot.models import *
urllib3.disable_warnings()
# initial Line Api Handler and Webhook.
_initialization = Initialization()
handler = _initialization.handler
line_bot_api = _initialization.line_bot_api

website_config = configparser.ConfigParser()
website_config.read("CrawlingSites.ini")
websites = website_config['TARGET_URL']
ReStart_Counter = 0

app = Flask(__name__)

"""
Define Fixed Reply
"""
REPLY_OK = "OK"
REPLY_FAIL = "SYSTEM_FAIL"

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return REPLY_OK

@app.route('/')
def hello_world():
    return "Hello,這是我的檢索型Line Bot 第一版！"

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    #actual_event_txt = event.message.text
    response_to_user_id = event.source.user_id
    type_of_event = str(type(event))
    if event.message.text == '科技新知':
        content = retrieveTechNews()  # get apple realtime news.
        # the line below cannot response to individual
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=content))
        return 0
    else:
        #_content = "Debug_Info:"+actual_event_txt + "##" + type_of_event#retrieveAppleNews()
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage("很抱歉，目前並無提供此種服務。"))
        return 0

################ Start OF Content Generation Functions ###############
def retrieveTechNews():
    #target_url = websites['TechNews']
    print('Starting get Tech News Data ...')
    rs = requests.session()
    res = rs.get(websites['TechNews'], verify=False)
    #res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    content = ""
    for index, data in enumerate(soup.select('article div h1.entry-title a')):
        if index == 12:
            return content
        title = data.text
        link = data['href']
        content += '{}\n{}\n\n'.format(title, link)
    return content

################ End OF Content Generation Functions #################

'''
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
  handler.line_bot_api.reply_message(event.reply_token, TextSendMessage(text=event.message.text))
'''

if __name__ == "__main__":
    #global ReStart_Counter
    #ReStart_Counter += 1
    print("ReStarting Count:{}".format(ReStart_Counter))
    app.run()
