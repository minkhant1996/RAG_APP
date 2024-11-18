
from dotenv import load_dotenv
import os
import yaml
from utils import DictToObject
import pytz
from datetime import datetime
# os.environ["TESSDATA_PREFIX"] = "/usr/share/tesseract-ocr/4.00/"

with open("config/yml_files/main_config.yml", "r") as ymlfile:
    config_dict = yaml.safe_load(ymlfile)


class Config:
    def __init__(self):
        config_obj = DictToObject(config_dict)
        environment = config_obj.ENVIRONMENT
        env_file = f"../.env.{environment}" if environment else ".env"
        env_file = ".env"
        load_dotenv(dotenv_path=env_file)

        self.redis_config = config_obj.REDIS
        self.timezone = pytz.timezone(config_obj.TIMEZONE)
        self.openai_key = os.getenv("OPENAI_API_KEY")
