import os
import requests
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)


class LLM:
    def __init__(self, model_name="gpt-4o-mini"):
        load_dotenv()
        self.model_url = "https://api.openai.com/v1/chat/completions"
        self.model_name = model_name
        self.api_key = os.getenv("API_KEY")
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        self.max_tokens = os.getenv("MAX_TOKENS")

    def get_llm_response(self, prompt):
        data = {
            "model": self.model_name,
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            "max_tokens": self.max_tokens,
        }

        llm_response = ""
        response = requests.post(
            self.model_url, headers=self.headers, json=data, timeout=50
        )
        if response.status_code == 200:
            llm_response = response.json()["choices"][0]["message"]["content"]
            logger.info(f"LLM response: {llm_response}\n\n\n")
        else:
            logger.error("Error:", response.status_code, response.text)

        return llm_response
