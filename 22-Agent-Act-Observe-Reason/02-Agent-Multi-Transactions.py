from google.generativeai import GenerativeModel
from google.generativeai.types.content_types import FunctionDeclaration
from google.generativeai.types.content_types import Tool
from google.generativeai import protos
import time

def add_numbers(num1: int, num2: int) -> int:
    """
    Adds two numbers and prints the operation.

    Args:
        num1 (int | float): The first number.
        num2 (int | float): The second number.

    Returns:
        int | float: The sum of num1 and num2.

    Example:
        >>> add_numbers(5, 3)
        In add_numbers(5, 3) = 8
        8
    """
    result = num1 + num2
    print(f"In add_numbers({num1}, {num2}) = {result}")
    return result


def multiply_numbers(num1: int, num2: int) -> int:
    """
    Multiplies two numbers and prints the operation.

    Args:
        num1 (int | float): The first number.
        num2 (int | float): The second number.

    Returns:
        int | float: The product of num1 and num2.

    Example:
        >>> multiply_numbers(4, 6)
        In multiply_numbers(4, 6) = 24
        24
    """
    result = num1 * num2
    print(f"In multiply_numbers({num1}, {num2}) = {result}")
    return result


def divide_numbers(num1: int, num2: int) -> int:
    """
    Performs integer (floor) division between two numbers and prints the operation.

    Args:
        num1 (int): The numerator.
        num2 (int): The denominator (must not be zero).

    Returns:
        int: The result of floor division (num1 // num2).

    Raises:
        ZeroDivisionError: If num2 is zero.

    Example:
        >>> divide_numbers(10, 3)
        In divide_numbers(10, 3) = 3
        3
    """
    result = num1 // num2
    print(f"In divide_numbers({num1}, {num2}) = {result}")
    return result

def declare_tools() -> Tool:
    """Declares tools for addition, multiplication, and division."""

    addition_func = FunctionDeclaration.from_function(add_numbers)
    multiplication_func = FunctionDeclaration.from_function(multiply_numbers)
    division_func = FunctionDeclaration.from_function(divide_numbers)

    ftools = [addition_func, multiplication_func, division_func]
    math_tool = Tool(function_declarations=ftools)

    return math_tool

def process_function_call(part):
    call = part.function_call
    func_name = call.name
    args = {key: value for key, value in call.args.items()}

    print(f"Invoking '{func_name}..{args}'")

    if func_name == "add_numbers":
        result = add_numbers(args['num1'], args['num2'])
    elif func_name == "multiply_numbers":
        result = multiply_numbers(args['num1'], args['num2'])
    elif func_name == "divide_numbers":
        result = divide_numbers(args['num1'], args['num2'])
    else:
        result = None

    fresponse = {"result" : result}
    tool_response = protos.FunctionResponse(
        name=func_name,
        response=fresponse
    )
    reply = protos.Part(function_response=tool_response)

    print()
    return reply

def call_model_loop(chat, prompt):

    # Interate till LLM asks invoke functions
    while True:
        print('{:*^50}'.format('prompt'))
        print(f"{prompt}\n")

        response = chat.send_message(prompt)
        print(f"Got reponse from LLM...")
        parts = response.candidates[0].content.parts
    
        has_function_call = False

        tool_response = []
        # Interate till all functions invoked
        for i, part in enumerate(parts, start=1):
            if part.function_call.name:
                has_function_call = True
                f_response = process_function_call(part)
                tool_response.append(f_response) 

        if not has_function_call and parts:
            print(f"LLM: NO function to Invoke...")
            return response
        elif not parts:
            print(f"call_model_loop: No parts in response")
            return "No response received"
        else:
            print(f"\nGoing back to LLM...\n")

        prompt = tool_response
    
    
def main():
    MODEL = "gemini-2.0-flash-001"
    tools = declare_tools()
    model = GenerativeModel(MODEL, tools=[tools])
    chat = model.start_chat()


    prompt = "Add 3 and 7. Multiply the output by 3. Divide the output by 5"
    # 3 + 7 = 10
    # 10 * 3 = 30
    # 30/5 = 6
    response = call_model_loop(chat, prompt)
    print(f"Final response :{response.text}")

if __name__ == "__main__":
    main()
