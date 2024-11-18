import redis
import json
import os
from datetime import datetime
import pytz

TIMEZONE = pytz.timezone("Asia/Bangkok")

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    db=0,  
    decode_responses=True 
)

class RedisDB_Manager:
    @staticmethod
    def save_to_redis(key, data):
        redis_client.set(key, json.dumps(data))
        
    @staticmethod
    def load_from_redis(key):
        try:
            data = redis_client.get(key)
            if data:
                return json.loads(data)
            return None
        except Exception as e:
            raise Exception(f"Error in load_from_redis: {str(e)}")
        
    @staticmethod
    def delete_from_redis(key):
        redis_client.delete(key)
    
    @staticmethod
    def initialize_user_data(redis_key, userId):
        try:
            UserData = {
                "userId": userId,
                "pdf": [],
                "chat_history": []
            }
            RedisDB_Manager.save_to_redis(redis_key, UserData)
            return UserData
        except Exception as e:
            raise Exception(f"Error in initialize_user_data: {str(e)}")
        
    @staticmethod
    def prepare_init_userdata(userId, pdf_filename, user_query):
        return {
                    "userId": userId,
                    "pdf": [
                            {
                                "pdf_filename": pdf_filename,
                                "pdf_title": None,
                                "image_path": []        
                            }
                        ],
                    "chat_history": [
                        {
                            "query": user_query,
                            "response": None,
                            "timestamp":
                                {
                                    "query": datetime.now(TIMEZONE).strftime("%Y-%m-%d %H:%M:%S"),
                                    "response": None
                                },
                            "input_tokens": None,
                            "output_tokens": None,
                        }    
                    ],
                }
