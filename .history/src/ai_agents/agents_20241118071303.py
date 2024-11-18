from llm import LLMBase
from utils import get_data_from_pattern


class AI_Agents:
    @staticmethod
    def get_the_prompts(content_type, main_prompt_info):
        prompt_info = get_data_from_pattern(rf'<{content_type}>\s*([\s\S]*?)\s*<{content_type}>', main_prompt_info)
        sys_pmt_ptn = "system_prompt"
        in_pm_ptn = "input_prompt"
        system_prompt = get_data_from_pattern(rf'<{sys_pmt_ptn}>\s*([\s\S]*?)\s*<{sys_pmt_ptn}>', prompt_info)
        input_prompt = get_data_from_pattern(rf'<{in_pm_ptn}>\s*([\s\S]*?)\s*<{in_pm_ptn}>', prompt_info)
        return system_prompt, input_prompt
        
    @staticmethod
    def find_main_title(list_titles: list, content_type: str = "Research"):
        with open("prompts/find_titles.txt", "r") as file:
            main_prompt_info = file.read()
            
        if content_type == "Research":
            with open("prompts/find_main_title.txt", "r") as file:
                main_prompt_info = file.read()
            system_prompt, input_prompt = AI_Agents.get_the_prompts(content_type, main_prompt_info)
            print(system_prompt)
            print()
            print(input_prompt)
        else:
            raise ValueError("Error in find_main_title: Invalid content type")
        
    @staticmethod
    def refine_query(query: str, main_prompt_info, content_type: str = "Research"):
        with open("prompts/refine_query.txt", "r") as file:
            main_prompt_info = file.read()
            
        if content_type == "Research":
            system_prompt, input_prompt = AI_Agents.get_the_prompts(content_type, main_prompt_info)
            print(system_prompt)
            print()
            print(input_prompt)
        else:
            raise ValueError("Error in refine_query: Invalid content type")
    
    @staticmethod
    def summarize_image(base64_image: str, content_type: str = "Research"):
        with open("prompts/image_summary.txt", "r") as file:
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
    

        