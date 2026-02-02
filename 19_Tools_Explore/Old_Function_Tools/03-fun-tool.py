from google.generativeai import GenerativeModel
from google.generativeai.types.content_types import FunctionDeclaration
from google.generativeai.types.content_types import Tool

def declare_fun_tools():
    is_even_func = FunctionDeclaration(
        name="is_even",
        description="Checks if a list of numbers are even.",
        parameters={
            "type": "object",
            "properties": {
                "numbers": {
                    "type": "array",
                    "items": {
                        "type": "integer",
                        "description": "A number to check."
                    },
                    "description": "The list of numbers to check."
                }
            },
            "required": ["numbers"]
        },
    )

    print(f"Created is_even FunctionDeclaration: {is_even_func}")
    is_even_tool = Tool(
        function_declarations=[is_even_func],
    )
    print(f"Created is_even Tool: {is_even_tool}")

    return is_even_tool


def is_even(numbers):  # Now takes a list of numbers
    print(f"Entering is_even with numbers: {numbers}")
    if not isinstance(numbers, list):
      raise TypeError("Input must be a list of integers")
    if not all(isinstance(num, int) for num in numbers):
      raise TypeError("All elements in the list must be integers")

    results = [num % 2 == 0 for num in numbers]
    print(f"Calling is_even({numbers}) = {results}")
    print(f"is_even({numbers}) result: {results}")
    print("Exiting is_even")
    return results

def extract_function_call(response):
    if response.candidates[0].content.parts[0].function_call:
        function_call = response.candidates[0].content.parts[0].function_call
        print(f"Extracted function call: {function_call}")
        return function_call

    print("No function call found. Exiting extract_function_call with None")
    return None

def execute_function(function_name, arguments):
    print(f"Entering execute_function with function_name: {function_name}, arguments: {arguments}")
    if function_name == "is_even":
        try:
            numbers = arguments["numbers"]
            print(f"numbers (before conversion): {numbers}")

            # Convert numbers to integers, handling potential errors
            int_numbers = []
            for num in numbers:
                try:
                    int_numbers.append(int(num))
                except (ValueError, TypeError):
                    print(f"Could not convert {num} to integer. Skipping.")
                    continue  # Skip non-integer value

            print(f"int_numbers (after conversion): {int_numbers}")

            print(f"Executing is_even with numbers: {int_numbers}")
            result = is_even(int_numbers)
            print(f"is_even execution result: {result}")
            print("Exiting execute_function with result")
            return result
        except (ValueError, TypeError) as e:
            print(f"Error during function execution: {e}")
            return "Error: Could not process numbers."  # Or raise, but LLM should know

    else:
        raise ValueError("Unknown function called.")


def generate_followup_prompt(result, prompt):
    print(f"Entering generate_followup_prompt with result: {result}, prompt: {prompt}")
    followup_prompt = f"The results of is_even are: {result}, against the prompt {prompt}, is it true?, Say Yes or No"
    print(f"Generated followup_prompt: {followup_prompt}")
    print("Exiting generate_followup_prompt")
    return followup_prompt

def handle_followup_response(followup_response):
    print("Entering handle_followup_response")
    print("Model's final response:", followup_response.candidates[0].content.parts[0].text)
    print("Exiting handle_followup_response")
    return followup_response

def call_model(model, prompt, tools=None):
    print(f"=============={prompt}==============")
    print(f"Entering call_model with prompt: {prompt}, tools: {tools}")
    response = model.generate_content(prompt, tools=tools)
    print(f"Model response: {response}")
    print("Exiting call_model")
    return response

def call_model_and_execute_tools(model, tool, prompt):
    print(f"Entering call_model_and_execute_tools with prompt: {prompt}")
    response = call_model(model, prompt, tools=[tool])
    function_call = extract_function_call(response)

    if function_call:
        function_name = function_call.name
        arguments = {key: value for key, value in function_call.args.items()}

        print(f"function_call :...\n{function_call}")
        print(f"function_name :{function_name}")
        print(f"arguments    :{arguments}")

        try:
            result = execute_function(function_name, arguments)
            if "Error" in result:  # Check for explicit error string
                return result

            followup_prompt = generate_followup_prompt(result, prompt)
            followup_response = call_model(model, followup_prompt)
        
            return handle_followup_response(followup_response)        
        except (ValueError, TypeError) as e:
            error_message = f"Error: {e}"
            print(error_message)
            return error_message

    print(response.text)
    print("Exiting call_model_and_execute_tools")
    return response.text


def main():
    MODEL = "gemini-2.0-flash-001"
    model = GenerativeModel(MODEL)

    tool = declare_fun_tools()

    prompt = "is 4 7 nine 19 are even numbers?"
    final_response = call_model_and_execute_tools(model, tool, prompt)
    print(final_response)


if __name__ == "__main__":
    main()
