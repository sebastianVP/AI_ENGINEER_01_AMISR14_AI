import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def create_openai_client()->OpenAI:
    """Crea un Cliente de OpenAI usando una API  key del entorno"""
    api_key = os.getenv("OPEN_API_KEY")
    if not api_key:
        raise RuntimeError(
            "Falta OPENAI_API_KEY. Configúrala en el archivo .env."
        )

    return OpenAI(api_key=api_key)
    
def get_model_name()->str:
    """Obtiene el modelo configurado para el proyecto"""
    model = os.getenv("OPENAI_MODEL")
    if not model:
        raise RuntimeError(
            "Falta OPENAI_MODEL. Configúrala en el archivo .env."
        )
    return model