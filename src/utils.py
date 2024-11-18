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
        if not isinstance(dictionary, dict):
            raise TypeError("Input must be a dictionary")

        for key, value in dictionary.items():
            try:
                if isinstance(value, dict):
                    setattr(self, key, DictToObject(value))
                else:
                    setattr(self, key, value)
            except Exception as e:
                raise RuntimeError(f"Error setting attribute '{key}' with value '{value}': {e}")

                
class ObjectToDict:
    @staticmethod
    def convert(obj):
        try:
            if not hasattr(obj, "__dict__"):
                return obj
            result = {}
            for key, value in obj.__dict__.items():
                if isinstance(value, DictToObject):  # Recursive call for nested objects
                    result[key] = ObjectToDict.convert(value)
                else:
                    result[key] = value
            return result
        except Exception as e:
            raise RuntimeError(f"Error converting object to dictionary: {e}")