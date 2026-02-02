from google.generativeai import GenerativeModel
from google.generativeai.types.content_types import FunctionDeclaration
from google.generativeai.types.content_types import Tool
import json

def is_even(number: int) -> bool:
    """Checks if a number is even."""
    return number % 2 == 0

def main():
    MODEL = "gemini-2.0-flash-001"
    is_even_func = FunctionDeclaration.from_function(is_even)
    is_even_tool = Tool(function_declarations=[is_even_func])
    model = GenerativeModel(MODEL)

    prompt = "Is 10 even?"
    response = model.generate_content(prompt, tools=[is_even_tool])
    print(json.dumps(response.to_dict(), sort_keys=True, indent=4))

    # ---- Individual prints with f-strings ----
    resp = response.to_dict()
    # print(f"model_version : {resp['model_version']}")
    # print(f"usage_metadata: {resp["usage_metadata"]}")

    candidate = resp["candidates"][0]
    print(f"candidates[0] : {candidate}")

    content = candidate["content"]
    print(f"candidates[0].content.role : {content['role']}")

    function_call = content["parts"][0]["function_call"]
    print(f"candidates[0].content.parts: {function_call}")

  
if __name__ == "__main__":
    main()
