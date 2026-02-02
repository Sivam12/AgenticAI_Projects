from google.generativeai import GenerativeModel
from google.generativeai.types.content_types import FunctionDeclaration
from google.generativeai.types.content_types import Tool

MODEL = "gemini-2.0-flash-001"

def is_even(number):
    print(f"Calling is_even({number})")
    return number % 2 == 0

def main():
    is_even_func = FunctionDeclaration(
        name="is_even",
        description="Checks if a number is even.",
        parameters={
            "type": "object",
            "properties": {
                "number": {
                    "type": "integer",
                    "description": "The number to check."
                }
            },
            "required": ["number"]
        },
    )

    is_even_tool = Tool(function_declarations=[is_even_func])

    model = GenerativeModel(MODEL)

    prompt = "Is 10 even?"

    response = model.generate_content(prompt, tools=[is_even_tool])
    print(response)
    
    if response.candidates[0].content.parts[0].function_call:
        function_call = response.candidates[0].content.parts[0].function_call
        function_name = function_call.name
        arguments = function_call.args

        if function_name == "is_even":
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

            follow_up_response = model.generate_content(
                contents=[function_response_content, user_message]
            )
            print(follow_up_response.text)
        else:
            print("Unknown function called")

    else:
        print(response.text)


if __name__ == "__main__":
    main()
