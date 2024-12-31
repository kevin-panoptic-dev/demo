import requests
from typing import Literal
from pprint import pprint
from pymodule.utility import prismelt
import dotenv
import os

dotenv.load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key={GEMINI_API_KEY}"
BASE = {"contents": [{"parts": [{"text": ""}]}]}
HEADER = {"Content-Type": "application/json"}


def fetch_data_from_gemini(
    *,
    message: str,
    prompt: str,
    language_message: str,
    type: Literal["validate", "translate"],
) -> dict:
    # prismelt("we are here!", color=(0, 0, 255))

    if not isinstance(message, str):
        raise TypeError("Gemini message must be a string")
    if not isinstance(prompt, str):
        raise TypeError("Gemini prompt must be a string")
    if not isinstance(language_message, str):
        raise TypeError("Gemini language_message must be a string")
    if type not in ["validate", "translate"]:
        raise ValueError("Gemini type must be either 'validate' or 'translate'")

    text = prompt + f"\n{language_message} \n\n" + f"User Message {message}"
    BASE["contents"][0]["parts"][0]["text"] = text
    response = requests.post(URL, json=BASE, headers=HEADER)
    if response.status_code == 200:
        finish_reason = response.json()["candidates"][0]["finishReason"]
        if finish_reason != "STOP":
            return {
                "error": "1",
                "error_message": "Unable to parse data by Gemini",
                "response": None,
            }
        else:
            response_text: str = response.json()["candidates"][0]["content"]["parts"][
                0
            ]["text"]
            if type == "validate":
                if response_text.strip("\n") == "0":
                    return {
                        "error": "0",
                        "error_message": None,
                        "response": response_text,
                    }
                else:
                    return {
                        "error": "1",
                        "error_message": "Unable to discern the user's input message",
                        "response": response_text,
                    }
            else:
                return {
                    "error": "0",
                    "error_message": None,
                    "response": response_text,
                }
    else:
        return {
            "error": "1",
            "error_message": "Unable to fetch data from Gemini",
            "response": None,
        }
