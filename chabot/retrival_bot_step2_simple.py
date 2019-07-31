from flask import Flask, request, abort
import requests
import re
import random
import configparser
import urllib3
from bs4 import BeautifulSoup
from initialization import Initialization
import json
import pandas as pd
import csv

'''import linebot sdk'''
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
urllib3.disable_warnings()
####### initial Line Api Handler and Webhook.######
_initialization = Initialization()
handler = _initialization.handler
line_bot_api = _initialization.line_bot_api
NEWLINE = '\n'

website_config = configparser.ConfigParser()
website_config.read("CrawlingSites.ini")
websites = website_config['TARGET_URL']

app = Flask(__name__)

"""
Define Fixed Reply
"""
REPLY_OK = "OK"
REPLY_FAIL = "SYSTEM_FAIL"



@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return REPLY_OK


@app.route('/')
def hello_world():
    return "Hello,這是我的檢索型Line Bot Ver 2 Simple！"


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    #actual_event_txt = event.message.text
    #response_to_user_id = event.source.user_id
    #type_of_event = str(type(event))
    ######## First Section of IF Statements #########
    if event.message.text == '科技新知':
        content = retrieveTechNews()  # get apple realtime news.
        # the line below cannot response to individual
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=content))
        return 0
    if event.message.text == '查詢臺股':
        #check if exists a stock query
        print("response id is {}".format(response_to_user_id))
        line_bot_api.reply_message(                                  
            event.reply_token, TextSendMessage(retrieveTWStock(2331)))
        return 0

    ######## End of First Section of IF Statements #########

    ######## Second Section of IF Statements:for button menu #########
    if event.message.text == '發發選單' or event.message.text == 'services':
        buttons_template = TemplateSendMessage(
            alt_text='服務選單',
            template=ButtonsTemplate(
                title='服務類型',
                text='請選擇',
                thumbnail_image_url='https://i.imgur.com/tXz0cel.png',
                ###前二種類型都為單純爬取資訊。第三、第四種，需要二輪的對話。閒聊服務，以Grammar為主的聊天實作。
                actions=[
                    MessageTemplateAction(
                        label='科技新知',
                        text='科技新知'
                    ),
                    MessageTemplateAction(
                        label='查詢臺股',
                        text='查詢臺股'
                    )
                ]
            )
        )
        print("response id is {}".format(response_to_user_id))
        line_bot_api.reply_message(event.reply_token, buttons_template)
        return 0
    else:
        _content = "Debug_Info:"+actual_event_txt + "##" + type_of_event#retrieveAppleNews()
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage("很抱歉，目前並無提供此種服務。"+_content))
            #event.reply_token, TextSendMessage("很抱歉，目前並無提供此種服務。"))
        return 0
    ######## End of Second Section of IF Statements:for button menu #########


################ Start Of Response Generation Functions ###############

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

def retrieveTWStock(stocknum=0000):
    rs=requests.session()
    res=rs.get(websites['TWSTOCK'].format(stocknum))
    qstock = json.loads(res.text)
    return processingStockData(qstock)

################ End OF Content Generation Functions #################

################ Processing Raw Data From Web ########################


def processingStockData(rawJson):
    # 過濾出有用到的欄位
    columns = ['c', 'n', 'z', 'tv', 'v', 'o', 'h', 'l', 'y']
    df = pd.DataFrame(rawJson['msgArray'], columns=columns)
    df.columns = ['股票代號', '公司簡稱', '當盤成交價', '當盤成交量',
                  '累積成交量', '開盤價', '最高價', '最低價', '昨收價']
    # 新增漲跌百分比
    df.iloc[:, [2, 3, 4, 5, 6, 7, 8]] = df.iloc[:,
                                                [2, 3, 4, 5, 6, 7, 8]].astype(float)
    df['漲跌百分比'] = (df['當盤成交價'] - df['昨收價'])/df['昨收價'] * 100
    stocklist = list(csv.reader(df.to_csv().splitlines()))
    _content = ""
    for idx in range(1, 10):
        _content = _content + stocklist[0][idx]+":"+stocklist[1][idx] + '\n'
    return _content

############### End of Processing Raw Data From Web ##################



if __name__ == "__main__":
    app.run()
