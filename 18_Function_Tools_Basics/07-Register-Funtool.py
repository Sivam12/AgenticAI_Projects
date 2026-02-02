from google.generativeai import GenerativeModel
from google.generativeai.types.content_types import FunctionDeclaration
from google.generativeai.types.content_types import Tool

def is_even(number: int) -> bool:
    """Checks if a number is even."""
    return number % 2 == 0

def main():
    MODEL = "gemini-2.0-flash-001"
    
    prompt = "Is 10 even?"

    is_even_func = FunctionDeclaration.from_function(is_even)
    print(is_even_func.to_proto())
    
    is_even_tool = Tool(function_declarations=[is_even_func])

    model = GenerativeModel(MODEL)
    response = model.generate_content(prompt, tools=[is_even_tool])

    print(response)
    
if __name__ == "__main__":
    main()
