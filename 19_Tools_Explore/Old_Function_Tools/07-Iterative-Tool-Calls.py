from google.generativeai import GenerativeModel
from google.generativeai.types.content_types import FunctionDeclaration
from google.generativeai.types.content_types import Tool
import time

# Tool declarations
def get_tool_declarations():
    tool_declarations = [Tool(function_declarations=[
        FunctionDeclaration(
            name="is_even",
            description="Check which numbers are even. Use this function to determine if numbers in a list are even. Accepts both integers and floats.",
            parameters={
                "type": "object",
                "properties": {
                    "numbers": {
                        "type": "array",
                        "items": {"type": "number"},
                        "description": "List of numbers to check for evenness."
                    }
                },
                "required": ["numbers"]
            }
        ),
        FunctionDeclaration(
            name="is_prime",
            description="Check which numbers are prime. Use this function to determine if numbers in a list are prime numbers. Accepts both integers and floats.",
            parameters={
                "type": "object",
                "properties": {
                    "numbers": {
                        "type": "array",
                        "items": {"type": "number"},
                        "description": "List of numbers to check for primality."
                    }
                },
                "required": ["numbers"]
            }
        )
    ])]
    return tool_declarations

def is_even(numbers):
    result = [n % 2 == 0 for n in numbers]
    return result

def is_prime(numbers):
    def check(n):
        if n <= 1: return False
        for i in range(2, int(n**0.5)+1):
            if n % i == 0: return False
        return True
    result = [check(n) for n in numbers]
    return result

def clean_numbers(numbers):
    cleaned = []
    for n in numbers:
        try:
            cleaned.append(int(float(n)))
        except Exception:
            print(f"Skipping invalid number: {n}")
    return cleaned

def generate_followup_prompt(numbers, results, func_name):
    if func_name == "is_even":
        even_numbers = [numbers[i] for i in range(len(numbers)) if results[i]]
        followup_prompt = (
            f"From the given the numbers {numbers}, is_even function idenfied {even_numbers} as even number(s)\n"
        )
    elif func_name == "is_prime":
        prime_numbers = [numbers[i] for i in range(len(numbers)) if results[i]]
        followup_prompt = (
            f"From the given the numbers {numbers}, is_prime function idenfied {prime_numbers} as prime number(s)\n"
        )
    else:
        followup_prompt = ""
    return followup_prompt

def get_model_response(model, prompt, tools):
    """Gets the model's response to a given prompt and tools."""
    print('{:*^50}'.format('prompt'))
    print(f"{prompt}\n")
    time.sleep(3)
    return model.generate_content(prompt, tools=tools)

def process_function_call(part):
    call = part.function_call
    func_name = call.name
    numbers = clean_numbers(call.args.get("numbers", []))
    print(f"Invoking '{func_name}' with args :{numbers}")

    if func_name == "is_even":
        result = is_even(numbers)
    elif func_name == "is_prime":
        result = is_prime(numbers)
    else:
        result = None

    print(f"    result :{result}")
    followup_prompt = generate_followup_prompt(numbers, result, func_name)
    return followup_prompt

def call_model_loop(model, prompt):
    tools = get_tool_declarations()
    orig_prompt = prompt

    while True:
        response = get_model_response(model, prompt, tools)
        parts = response.candidates[0].content.parts
        print(f"response :\n{response}\n")

        has_function_call = False
        new_prompt = ""

        for i, part in enumerate(parts, start=1):
            if hasattr(part, "function_call") and part.function_call.name != '':
                has_function_call = True
                followup_prompt = process_function_call(part)
                new_prompt += followup_prompt

        if not has_function_call and parts:
            final_text = "".join(part.text for part in parts if hasattr(part, "text"))
            return final_text
        elif not parts:
            print(f"call_model_loop: No parts in response")
            return "No response received"
        else:
            print(f"\nGoing back to LLM...\n")

        prompt = (
            f"After invocation of functions the results are...\n"
            f"{new_prompt}\n"
            f"From above results can you build the answer to the question {orig_prompt}"
        )

def main():
    # MODEL = "gemini-2.0-flash"
    MODEL = "gemini-1.5-flash"
    model = GenerativeModel(MODEL)

    prompt = "Which numbers are even and which are prime in this list: 4, 7, nine, 19, 23 and two?"
    answer = call_model_loop(model, prompt)
    
    print(f"\nFinal Response :\n{answer}")

if __name__ == "__main__":
    main()
