import configparser
from linebot import (
    LineBotApi, WebhookHandler
)


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Initialization(metaclass=Singleton):
    SETTING_FILE = "setting.config"
    def __init__(self, file=SETTING_FILE):
        self.config = configparser.ConfigParser()
        self.check_file(file)
        self.Channel_Access_Token = self.config['LINE_BOT_CONGIGURE']['Channel_Access_Token']
        self.Channel_Secret = self.config['LINE_BOT_CONGIGURE']['Channel_Secret']
        self.Channel_User_ID = self.config['LINE_BOT_CONGIGURE']['Channel_User_ID']
        self.handler = None
        self.line_bot_api = None
        self.line_bot_init()

    def check_file(self, file):
        self.config.read(file)
        if not self.config.sections():
            raise configparser.Error('setting.config not exists')

    def line_bot_init(self):
        self.handler = WebhookHandler(self.Channel_Secret)
        self.line_bot_api = LineBotApi(self.Channel_Access_Token)
