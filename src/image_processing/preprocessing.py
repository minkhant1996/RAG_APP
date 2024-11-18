import base64
from PIL import Image
import numpy as np
import os, io

class ImageProcessor:
    @staticmethod
    def base64_to_image(base64_string: str):
        image_data = base64.b64decode(base64_string)
        return Image.open(io.BytesIO(image_data))
    
    
    @staticmethod
    def save_image_local(image_data: any, save_path: str, file_name: str, extension: str):
        os.makedirs(save_path, exist_ok=True)  # Ensure the directory exists
        full_path = os.path.join(save_path, f"{file_name}.{extension}")
        
        # If `image_data` is a PIL Image
        if isinstance(image_data, Image.Image):
            image_data.save(full_path)
        
        # If `image_data` is a Base64-encoded string
        elif isinstance(image_data, str):                
            with open(full_path, "wb") as f:
                f.write(base64.b64decode(image_data))

        # If `image_data` is a NumPy array
        elif isinstance(image_data, np.ndarray):
            pil_image = Image.fromarray(image_data)
            pil_image.save(full_path)
        
        # If `image_data` is raw bytes
        elif isinstance(image_data, (bytes, bytearray)):
            with open(full_path, "wb") as f:
                f.write(image_data)
        
        # If `image_data` is a file path
        elif isinstance(image_data, str) and os.path.isfile(image_data):
            with open(image_data, "rb") as src, open(full_path, "wb") as dest:
                dest.write(src.read())
        
        else:
            raise ValueError("Unsupported image_data type")

