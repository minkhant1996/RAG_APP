import tiktoken
from dotenv import load_dotenv
load_dotenv()
import os
from openai import OpenAI
import base64
import numpy as np
from PIL import Image
from io import BytesIO
from config import Config

config = Config()

client = OpenAI()
client.api_key = config.openai_key

class LLMBase:
    @staticmethod
    def estimate_token(context):
        try:
            encoding = tiktoken.encoding_for_model("gpt-4o")
            encoded_text = encoding.encode(context)
            return len(encoded_text)
        except Exception as e:
            raise RuntimeError(f"Error in estimate_token: {e}")

    
    @staticmethod
    def get_chat_prompt(system_prompt, user_prompt, base64_images):
        try:
            user_content = [{"type": "text", "text": user_prompt}]
            
            if base64_images:
                user_content += [
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image}", "detail": "high"}} 
                    for image in base64_images
                ]

            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ]
            
            return messages
        except Exception as e:
            raise RuntimeError(f"Error in get_chat_prompt: {e}")


    @staticmethod
    def get_response_openai(system_prompt, user_prompt, model, max_tokens, temperature=0.8, top_p=0.9, base64_images=[]):
        try:
            messages = LLMBase.get_chat_prompt(system_prompt, user_prompt, base64_images)
            input_tokens = LLMBase.estimate_token(system_prompt) + LLMBase.estimate_token(user_prompt)
            
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens, 
                temperature=temperature,
                top_p=top_p,
            )
            
            botResponse = response.choices[0].message.content
            output_tokens = LLMBase.estimate_token(botResponse)
            
            return input_tokens, output_tokens, botResponse
        except KeyError as e:
            raise RuntimeError(f"Error in get_response_openai: Missing key in response or parameter - {e}")
        except AttributeError as e:
            raise RuntimeError(f"Error in get_response_openai: Invalid attribute in response or client object - {e}")
        except Exception as e:
            raise RuntimeError(f"Error in get_response_openai: {e}")
