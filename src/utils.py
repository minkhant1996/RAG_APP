import re

def get_data_from_pattern(pattern: str, text: str):
    try:
        extracted_data = re.search(pattern, text)
        return extracted_data.group(1) if extracted_data else None
    except re.error as e:
        raise RuntimeError(f"Error in get_data_from_pattern: Invalid regex pattern - {e}")
    except Exception as e:
        raise RuntimeError(f"Error in get_data_from_pattern: {e}")
    
class DictToObject:
    def __init__(self, dictionary):
        for key, value in dictionary.items():
            if isinstance(value, dict):
                setattr(self, key, DictToObject(value))
            else:
                setattr(self, key, value)
                
class ObjectToDict:
    @staticmethod
    def convert(obj):
        if not hasattr(obj, "__dict__"):
            return obj
        result = {}
        for key, value in obj.__dict__.items():
            if isinstance(value, DictToObject):  # Recursive call for nested objects
                result[key] = ObjectToDict.convert(value)
            else:
                result[key] = value
        return result
