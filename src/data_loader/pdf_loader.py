from unstructured.partition.pdf import partition_pdf
from unstructured.staging.base import elements_to_dicts
from bs4 import BeautifulSoup
from ai_agents import AI_Agents
from image_processing import ImageProcessor
from typing import Optional, IO
import gc, os, re
from utils import get_data_from_pattern
from config import Config

config = Config()

class PDF_Reader:
    def __init__(
            self,
            userId: str,
            pdf_filename: str,
            pdf_path: Optional[str] = None,
            pdf_file: Optional[IO[bytes]] = None,
            content_type: str = "Research",
            strategy: str = "hi_res",
            languages: list[str] = ["eng"],
            infer_table_structure: bool = True,
            model_name: str = "yolox",
            extract_image_block_types: list[str] = ["Image", "Table"],
            extract_image_block_to_payload: bool = True,
            extract_images_in_pdf: bool = True,
            convert_table_html_to_text: bool = False,
            save_image: bool = False,
            save_pdf_text: bool = False,
            summarize_image: bool = False
    ):
        self.userId = userId
        self.pdf_filename = pdf_filename
        self.pdf_path = pdf_path
        self.pdf_file = pdf_file
        self.strategy = strategy
        self.languages = languages
        self.infer_table_structure = infer_table_structure
        self.model_name = model_name
        self.extract_image_block_types = extract_image_block_types
        self.extract_image_block_to_payload = extract_image_block_to_payload
        self.extract_images_in_pdf = extract_images_in_pdf
        self.convert_table_html_to_text = convert_table_html_to_text
        self.save_image = save_image
        self.save_pdf_text = save_pdf_text
        self.content_type = content_type
        self.summarize_image = summarize_image
        self.pdf_element_dict = None
        
    def process_pdf(self):
        self.get_pdf_content_elements()
        return self.process_pdf_elements()

    def get_pdf_content_elements(self):
        try:
            elements = partition_pdf(
                filename=self.pdf_path if self.pdf_path else None,
                file=self.pdf_file if self.pdf_file else None,
                strategy=self.strategy,
                languages=self.languages,
                infer_table_structure=self.infer_table_structure,
                model_name=self.model_name,
                extract_image_block_types=self.extract_image_block_types,
                extract_image_block_to_payload=self.extract_image_block_to_payload,
                extract_images_in_pdf=self.extract_images_in_pdf
            )
            self.pdf_element_dict = elements_to_dicts(elements) # return a list
            
            # clear cache and free up memory
            del elements
            gc.collect()
            
        except Exception as e:
            raise ValueError(f"Error in processing PDF: {e}")

    def process_pdf_elements(self):
        try:
            extracted_info = ""
            title_list = [pdf_element["text"] for pdf_element in self.pdf_element_dict if pdf_element["type"] == "Title"]
            # main_title = title_list[0] if title_list else None
            main_title, other_titles = AI_Agents.find_titles(title_list, self.content_type)
            extracted_info += "List of Titles: " + ", ".join(title_list) + "\n\n"
            
            for ele_idx, pdf_element in enumerate(self.pdf_element_dict):
                if pdf_element["type"] == "Table":
                    extracted_info += self.html_to_text(pdf_element["metadata"]["text_as_html"]) + "\n"  if self.convert_table_html_to_text else pdf_element["metadata"]["text_as_html"] + "\n"

                elif pdf_element["type"] == "Image":
                    base64_image = pdf_element["metadata"]["image_base64"]
                    figure_name = self.get_figure_name(self.pdf_element_dict[max(0, ele_idx - 2): ele_idx + 3]) # only element get 2 previous and 2 next elements to process figure caption
                    
                    if figure_name:
                        if self.save_image:
                            ImageProcessor.save_image_local(
                                        image_data= base64_image, 
                                        save_path = f"{config.user_config.user_data_path}/{self.userId}",
                                        file_name = figure_name,
                                        extension = "png"
                                    )
                            
                        extracted_info +=  f"###IMAGE###{figure_name}###IMAGE###" + "\n" 
                        
                        if self.summarize_image:
                            summarized_text = AI_Agents.summarize_image(base64_image, self.content_type)
                            extracted_info += f"Summary for {figure_name}: " + summarized_text + "\n"
                    else:
                        extracted_info += pdf_element["text"] + "\n"
                    
                elif pdf_element["type"] == "Title":
                    if pdf_element["text"] in other_titles or pdf_element["text"] == main_title:
                        extracted_info += "\n\n"  + pdf_element["text"] + "\n" 
                    else:
                        extracted_info += pdf_element["text"] + "\n" # Not real titles, Treat as normal text
                    
                elif pdf_element["type"] == "Header":
                    pass
                
                else: # for the rest: ListItem, NarrativeText, FigureCaption, UncategorizedText, Etc
                    extracted_info += pdf_element["text"] + "\n"  
        
            if self.save_pdf_text:
                file_path = f"{config.user_config.user_data_path}/{self.userId}"
                os.makedirs(file_path, exist_ok=True)
                self.save_pdf_text_local(os.path.join(file_path, f"{self.pdf_filename}.txt"), extracted_info)
            
            return extracted_info, main_title, other_titles
        except Exception as e:
            raise ValueError(f"Error in processing PDF elements: {e}")
            
    
    def save_pdf_text_local(self, file_path, text):
        try:
            with open(file_path, "w") as file:
                file.write(text)
        except Exception as e:
            raise ValueError(f"Error in saving PDF text: {e}")

    def get_figure_name(self, pdf_element: list):
        try:
            tmp_caption = ""
            for tmp_element in pdf_element:
                if tmp_element["type"] == "FigureCaption":
                    tmp_caption += tmp_element["text"] + "\n"
                    
            pattern = r"Figure (\d+):"
            
            if tmp_caption:
                image_number = get_data_from_pattern(pattern, tmp_caption)
                if image_number:
                    return f"Figure-{image_number}" 
                
            return None 
        except Exception as e:
            raise ValueError(f"Error in getting figure name: {e}")

            
    def html_to_text(self, html_text: str):
        try:
            table_html = "<table>" + html_text + "</table>"
            soup = BeautifulSoup(table_html, "html.parser")
            rows = soup.find_all("tr")
            return "\n".join(" | ".join(cell.get_text(strip=True) for cell in row.find_all("td")) for row in rows)
        except Exception as e:
            raise ValueError(f"Error in converting HTML to text: {e}")
