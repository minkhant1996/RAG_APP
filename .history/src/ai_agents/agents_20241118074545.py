from llm import LLMBase
from utils import get_data_from_pattern
import json
from config import Config
import os

config = Config()

class AI_Agents:
    @staticmethod
    def get_the_prompts(content_type, main_prompt_info):
        prompt_info = get_data_from_pattern(rf'<{content_type}>\s*([\s\S]*?)\s*<{content_type}>', main_prompt_info)
        sys_pmt_ptn = config.prompt_config.trigger_words.system_prompt
        in_pm_ptn = config.prompt_config.trigger_words.input_prompt
        system_prompt = get_data_from_pattern(rf'<{sys_pmt_ptn}>\s*([\s\S]*?)\s*<{sys_pmt_ptn}>', prompt_info)
        input_prompt = get_data_from_pattern(rf'<{in_pm_ptn}>\s*([\s\S]*?)\s*<{in_pm_ptn}>', prompt_info)
        return system_prompt, input_prompt
        
    @staticmethod
    def find_titles(list_titles: list, content_type: str = "Research"):
        with open(config.prompt_config.prompt_files.find_titles, "r") as file:
            main_prompt_info = file.read()
            
        if content_type == "Research":
            system_prompt, input_prompt = AI_Agents.get_the_prompts(content_type, main_prompt_info)
            list_titles_str = "\n".join(list_titles)
            print(system_prompt)
            print()
            print(input_prompt)
            response = LLMBase.get_response_openai(system_prompt, input_prompt, "gpt-4o-mini", 300)
            
            json_data_str = response[2].replace("```json", "").replace("```", "")
            json_data = json.loads(json_data_str)
            main_title, other_titles = json_data["main_title"], json_data["other_titles"]
            return main_title, other_titles
        else:
            raise ValueError("Error in find_main_title: Invalid content type")
        
    @staticmethod
    def refine_query(query: str, main_prompt_info, content_type: str = "Research"):
        with open(config.prompt_config.prompt_files.refine_query, "r") as file:
            main_prompt_info = file.read()
            
        if content_type == "Research":
            system_prompt, input_prompt = AI_Agents.get_the_prompts(content_type, main_prompt_info)
            print(system_prompt)
            print()
            print(input_prompt)
            response = LLMBase.get_response_openai(system_prompt, input_prompt, "gpt-4o-mini", 300, query=query)
            return response[2]
        else:
            raise ValueError("Error in refine_query: Invalid content type")
    
    @staticmethod
    def summarize_image(base64_image: str, content_type: str = "Research"):
        with open(config.prompt_config.prompt_files.image_summary, "r") as file:
            main_prompt_info = file.read()
            
        if content_type == "Research":
            system_prompt, input_prompt = AI_Agents.get_the_prompts(content_type, main_prompt_info)
            print(system_prompt)
            print()
            print(input_prompt)
        else:
            raise ValueError("Error in summarize_image: Invalid content type")
            
        response = LLMBase.get_response_openai(system_prompt, input_prompt, "gpt-4o-mini", 300, base64_images=[base64_image])
        return response[2]
    

        