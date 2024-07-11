import os
import json

def load_config():
    config = {
        "openai_api_key": os.environ.get("OPENAI_API_KEY"),
        "google_cloud_credentials": json.loads(os.environ.get("GOOGLE_CLOUD_CREDENTIALS", "{}"))
    }
    
    if not config["openai_api_key"]:
        raise ValueError("OPENAI_API_KEY environment variable is not set")
    
    if not config["google_cloud_credentials"]:
        raise ValueError("GOOGLE_CLOUD_CREDENTIALS environment variable is not set")
    
    return config