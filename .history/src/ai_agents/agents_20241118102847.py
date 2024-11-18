from llm import LLMBase
from utils import get_data_from_pattern
import json
from config import Config
import os
from retriever import Retriever

config = Config()

class AI_Agents:
    @staticmethod
    def get_the_prompts(content_type, main_prompt_info):
        prompt_info = get_data_from_pattern(rf'<{content_type}>\s*([\s\S]*?)\s*<{content_type}>', main_prompt_info)
        if prompt_info is None:
            prompt_info = main_prompt_info
        sys_pmt_ptn = config.prompt_config.trigger_words.system_prompt
        in_pm_ptn = config.prompt_config.trigger_words.input_prompt
        print(sys_pmt_ptn, in_pm_ptn)
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
            input_prompt = input_prompt.replace("###LIST_TITLES###", list_titles_str)
            response = LLMBase.get_response_openai(system_prompt, input_prompt, "gpt-4o-mini", 500)
            
            json_data_str = response[2].replace("```json", "").replace("```", "")
            json_data = json.loads(json_data_str)
            main_title, other_titles = json_data["main_title"], json_data["other_titles"]
            return main_title, other_titles
        else:
            raise ValueError("Error in find_main_title: Invalid content type")
        
    @staticmethod
    def refine_query(query: str, main_prompt_info: str, main_titles: list, content_type: str = "Research"):
        with open(config.prompt_config.prompt_files.refine_query, "r") as file:
            main_prompt_info = file.read()
            
        if content_type == "Research":
            system_prompt, input_prompt = AI_Agents.get_the_prompts(content_type, main_prompt_info)
            input_prompt = input_prompt.replace(
                                            "###CONTENT_TYPE###", query).replace(
                                                "###TOPICS###", str(main_titles)).replace(
                                                    "###USER_QUERY###", query)
            response = LLMBase.get_response_openai(system_prompt, input_prompt, "gpt-4o-mini", 300)
            return response[2]
        else:
            raise ValueError("Error in refine_query: Invalid content type")
    
    @staticmethod
    def summarize_image(base64_image: str, content_type: str = "Research"):
        with open(config.prompt_config.prompt_files.image_summary, "r") as file:
            main_prompt_info = file.read()
            
        if content_type == "Research":
            system_prompt, input_prompt = AI_Agents.get_the_prompts(content_type, main_prompt_info)
        else:
            raise ValueError("Error in summarize_image: Invalid content type")
            
        response = LLMBase.get_response_openai(system_prompt, input_prompt, "gpt-4o-mini", 300, base64_images=[base64_image])
        return response[2]
    

    @staticmethod
    def intent_detection(query: str, docs: list, content_type: str = "Research"):
        with open(config.prompt_config.prompt_files.intent_detection, "r") as file:
            main_prompt_info = file.read()
        if content_type == "Research":
            docs_str = ""
            for i, doc in enumerate(docs):
                docs_str += f"Doc {i+1}: {str(doc)}\n"
            system_prompt, input_prompt = AI_Agents.get_the_prompts(content_type, main_prompt_info)
            input_prompt = input_prompt.replace(
                                                "###CONTENT_TYPE###", content_type).replace(
                                                    "###DOCS###", docs_str).replace(
                                                        "###USER_QUERY###", query)
        else:
            raise ValueError("Error in intent_detection: Invalid content type")
            
        response = LLMBase.get_response_openai(system_prompt, input_prompt, "gpt-4o-mini", 300)
        return response[2]
    
    @staticmethod
    def chatbot_response(userId: str, query: str, user_data: dict, content_type: str = "Research"):
        with open(config.prompt_config.prompt_files.chatbot_response, "r") as file:
            main_prompt_info = file.read()
            
        system_prompt, input_prompt = AI_Agents.get_the_prompts(content_type, main_prompt_info)
        chat_history = AI_Agents.prepeare_chat_history(user_data["chat_history"])
        extracted_knowledge = "No documents found"
        input_prompt = input_prompt.replace("###CHAT_HISTORY###", chat_history)
        
        if content_type == "Research":
            docs = AI_Agents.get_titles(user_data["pdf"])
            intent_detection = AI_Agents.intent_detection(query, docs, content_type)
            
            if intent_detection.lower().strip() == "true": # Only relevant extract documents
                main_titles = [pdf["pdf_title"] for pdf in user_data["pdf"]]
                refine_query = AI_Agents.refine_query(query, main_prompt_info, main_titles, content_type)
                for text_split_method in config.rag_config.retrieve.text_split_methods:
                    retriever = Retriever(
                        vector_store_local_path=f"{config.User_Data_Local.user_data_path}/{userId}/{text_split_method}/faiss_index",
                        vectors_store_type="faiss",
                        retrieve_type=config.rag_config.retrieve.retrieve_type
                    )
                    extracted_knowledge = retriever.retrieve(refine_query)
                
            input_prompt = input_prompt.replace("###DOCS###", extracted_knowledge)
            
            # chat_history_str = "\n".join(chat_history)
            # input_prompt = input_prompt.replace("###CHAT_HISTORY###", chat_history_str)
            # response = LLMBase.get_response_openai(system_prompt, input_prompt, "gpt-4o-mini", 300, query=query)
            return ""
        else:
            raise ValueError("Error in chatbot_response: Invalid content type")
    
    @staticmethod
    def get_titles(pdf_list: list):
        titles = []
        for pdf in pdf_list:
            titles.append(
                {
                "main_title": pdf["pdf_title"],
                "other_titles": pdf["other_titles"]
                })
        return titles
    @staticmethod
    def prepeare_chat_history(chat_history: list):
        chat_history_str = ""
        chat_history = chat_history[-config.chat_bot_config.chat_history_length:]
        for chat in chat_history[-config.chat_bot_config.chat_history_length:]:
            chat_history_str += f"User: {chat['query']}\nChatbot: {chat['response']}\n"
        return chat_history_str