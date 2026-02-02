from google.generativeai import GenerativeModel
from google.generativeai.types.content_types import FunctionDeclaration
from google.generativeai.types.content_types import Tool

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
    
    print(response.candidates[0].content.parts[0])
     
    # Processing Tool Request 
    function_call = response.candidates[0].content.parts[0].function_call
    function_name = function_call.name
    arguments = function_call.args
    number = arguments["number"]

    result = is_even(number) 
    
    function_response_content = {
        "role": "function",
        "parts": [
            {
                "function_response": {
                    "name": function_name,
                    "response": {"result": result},
                }
            }
        ],
    }
    
    user_message = {"role": "user", "parts": [prompt]}
    final_message = [function_response_content, user_message]
    # final_message = [function_response_content]
    
    follow_up_response = model.generate_content(contents=final_message)
    print(follow_up_response.text)
    
if __name__ == "__main__":
    main()
