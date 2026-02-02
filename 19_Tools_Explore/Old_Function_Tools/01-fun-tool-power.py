from google.generativeai import GenerativeModel
from google.generativeai.types.content_types import FunctionDeclaration
from google.generativeai.types.content_types import Tool

def is_even(number):
    if not isinstance(number, int):
        print(f"TypeError: Input must be an integer, but got {type(number)}")
        raise TypeError("Input must be an integer")

    result = number % 2 == 0

    print(f"Calling is_even({number}) = {result}")
    return result

def declare_fun_tools():
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

    return is_even_tool

def extract_function_call(response):
    if response.candidates[0].content.parts[0].function_call:
        function_call = response.candidates[0].content.parts[0].function_call
        return function_call
    
    print("No function call found. Exiting extract_function_call with None")
    return None

def execute_function(function_name, arguments):
    if function_name == "is_even":
        try:
            number = int(arguments["number"])
            result = is_even(number)
            return result
        except (ValueError, TypeError) as e:
            print(f"Error during function execution: {e}")
            raise
    else:
        print(f"ValueError: Unknown function called: {function_name}")
        raise ValueError("Unknown function called.")

def generate_followup_prompt(result, prompt):
    followup_prompt = f"The result of is_even is: {result}, against the prompt {prompt}, is it true?"
    return followup_prompt

def call_model(model, prompt, tools=None):
    print(f"==============prompt==============")
    print(f"{prompt}")
    print()
    response = model.generate_content(prompt, tools=tools)
    return response

def call_model_and_execute_tools(model, tool, prompt):
    response = call_model(model, prompt, tools=[tool])
    print("Got response...")
    function_call = extract_function_call(response)

    if not function_call:
        print(response.text)
        print(f"Model response: {response.text}")
        print("Exiting call_model_and_execute_tools")
        return response.text

    function_name = function_call.name
    arguments = {key: value for key, value in function_call.args.items()}

    print(f"function_name :{function_name}")
    print(f"arguments    :{arguments}")

    try:
        result = execute_function(function_name, arguments)
        followup_prompt = generate_followup_prompt(result, prompt)
        followup_response = call_model(model, followup_prompt)
        return followup_response
    except (ValueError, TypeError) as e:
        error_message = f"Error: {e}"
        print(error_message)
        print(f"Error during function execution: {e}")
        return error_message


def main():
    MODEL = "gemini-2.0-flash-001"

    print("Starting main function")
    model = GenerativeModel(MODEL)
    print("Initialized GenerativeModel")
    
    tool = declare_fun_tools()
    print("Declared function tools")
    
    prompt1 = "Is 10 even?"
    print(f"Calling call_model_and_execute_tools with prompt: {prompt1}")
    final_response1 = call_model_and_execute_tools(model, tool, prompt1)
    print(f"Final response for prompt1: {final_response1}")

    prompt2 = "Is abc even?"
    final_response2 = call_model_and_execute_tools(model, tool, prompt2)
    print(f"Final response for prompt2: {final_response2}")


if __name__ == "__main__":
    main()
