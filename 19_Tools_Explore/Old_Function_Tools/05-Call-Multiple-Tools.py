from google.generativeai import GenerativeModel
from google.generativeai.types.content_types import FunctionDeclaration
from google.generativeai.types.content_types import Tool

def get_tool_declarations():
    tool_declarations = [Tool(function_declarations=[
        FunctionDeclaration(
            name="is_even",
            description="Check which numbers are even.",
            parameters={
                "type": "object",
                "properties": {
                    "numbers": {
                        "type": "array",
                        "items": {"type": "number"},
                        "description": "List of numbers to check."
                    }
                },
                "required": ["numbers"]
            }
        ),
        FunctionDeclaration(
            name="is_prime",
            description="Check which numbers are prime.",
            parameters={
                "type": "object",
                "properties": {
                    "numbers": {
                        "type": "array",
                        "items": {"type": "number"},
                        "description": "List of numbers to check."
                    }
                },
                "required": ["numbers"]
            }
        )
    ])]
    return tool_declarations

def is_even(numbers):
    print(f"is_even: numbers: {numbers}")
    result = [n % 2 == 0 for n in numbers]
    print(f"is_even: Result: {result}")
    return result

def is_prime(numbers):
    print(f"is_prime: numbers: {numbers}")
    def check(n):
        if n <= 1: return False
        for i in range(2, int(n**0.5)+1):
            if n % i == 0: return False
        return True
    result = [check(n) for n in numbers]
    print(f"is_prime: Result: {result}")
    return result

def clean_numbers(numbers):
    print(f"clean_numbers: numbers: {numbers}")
    cleaned = []
    for n in numbers:
        try:
            cleaned.append(int(float(n)))
        except Exception:
            print(f"Skipping invalid number: {n}")
    print(f"clean_numbers: Cleaned numbers: {cleaned}")
    return cleaned

def call_model_loop(model, prompt):
    print(f"==============Prompt: {prompt}==============\n")
    tools = get_tool_declarations()

    response = model.generate_content(prompt, tools=tools)
    print(f"call_model_loop: Response received")

    parts = response.candidates[0].content.parts
    print(f"parts len :{len(parts)}")

    for part in parts:
        if hasattr(part, "function_call"):
            call = part.function_call
            func_name = call.name
            print(f"\nFunction Call Detected:")
            print(f"  Name: {call.name}")
            arguments = {key: value for key, value in call.args.items()}
            print(f"  Arguments: {arguments}")

            numbers = clean_numbers(call.args.get("numbers", []))

            print(f"\nCalling {func_name} with: {numbers}")

            # Execute tool
            if func_name == "is_even":
                result = is_even(numbers)
            elif func_name == "is_prime":
                result = is_prime(numbers)
            else:
                result = None
            print(f"Result: {result}")

            function_response = {
                "function_response": {
                    "name": func_name,
                    "response": result
                }
            }
            
            print(f"\nFunction Response")
            print(function_response)
        else:
            print(f"No Function to call")

def main():
    MODEL = "gemini-2.0-flash-001"
    model = GenerativeModel(MODEL)
    prompt = "Which numbers are even and which are prime in this list: 4, 7, nine, 19, 23?"
    call_model_loop(model, prompt)

if __name__ == "__main__":
    main()
