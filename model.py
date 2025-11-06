from parse_config import get_api_key
from langchain_google_genai import ChatGoogleGenerativeAI
import os

def get_llm()->ChatGoogleGenerativeAI:
    api_key = get_api_key()

    if "GOOGLE_API_KEY" not in os.environ:
        os.environ["GOOGLE_API_KEY"] = api_key

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2
    )

    return llm