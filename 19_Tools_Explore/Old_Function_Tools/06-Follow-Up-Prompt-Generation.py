from google.generativeai import GenerativeModel
from google.generativeai.types.content_types import FunctionDeclaration
from google.generativeai.types.content_types import Tool

# Tool declarations
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
    return [n % 2 == 0 for n in numbers]

def is_prime(numbers):
    def check(n):
        if n <= 1: return False
        for i in range(2, int(n**0.5)+1):
            if n % i == 0: return False
        return True
    return [check(n) for n in numbers]

def clean_numbers(numbers):
    cleaned = []
    for n in numbers:
        try:
            cleaned.append(int(float(n)))
        except Exception:
            print(f"Skipping invalid number: {n}")
    return cleaned

def generate_followup_prompt(numbers, results, func_name):
    """Generates a prompt for the LLM based on the tool results."""
    if func_name == "is_even":
        even_numbers = [numbers[i] for i in range(len(numbers)) if results[i]]
        non_even_numbers = [numbers[i] for i in range(len(numbers)) if not results[i]]
        followup_prompt = (
            f"Given the numbers {numbers}, the even numbers are {even_numbers}, and the non-even numbers are {non_even_numbers}. "
            f"Identify which of the original numbers are prime and provide the results in a dictionary format like this: "
            f"{{number: 'Even/Odd/Prime'}}. Do not explain the reasoning."
        )
    elif func_name == "is_prime":
        prime_numbers = [numbers[i] for i in range(len(numbers)) if results[i]]
        non_prime_numbers = [numbers[i] for i in range(len(numbers)) if not results[i]]
        followup_prompt = (
            f"Given the numbers {numbers}, the prime numbers are {prime_numbers}, and the non-prime numbers are {non_prime_numbers}. "
            f"Identify which of the original numbers are even/odd and provide the results in a dictionary format like this: "
            f"{{number: 'Even/Odd/Prime'}}. Do not explain the reasoning."
        )
    else:
        followup_prompt = ""
    return followup_prompt


# Loop using generate_content
def call_model_loop(model, prompt):
    print(f"==============Prompt: {prompt}==============\n")
    tools = get_tool_declarations()

    response = model.generate_content(prompt, tools=tools)
    print(f"call_model_loop: Response received")

    parts = response.candidates[0].content.parts    
    print(f"parts len :{len(parts)}")

    for part in parts:
        call = part.function_call
        print(f"Fun name :{call.name}")
        print(f"Args     :{call.args.get("numbers", [])}")
        
    if parts and len(parts) > 0 and hasattr(parts[0], "function_call"):
        call = parts[0].function_call
        func_name = call.name
        numbers = clean_numbers(call.args.get("numbers", []))
        print(f"\nCalling {func_name} with: {numbers}")

        # Execute tool
        if func_name == "is_even":
            result = is_even(numbers)
        elif func_name == "is_prime":
            result = is_prime(numbers)
        else:
            result = None

        followup_prompt = generate_followup_prompt(numbers, result, func_name)

        print(f"Result: {result}")
        print(f"followup_prompt {followup_prompt}")

        # Send the follow-up prompt in a single turn
        response = model.generate_content(followup_prompt)

        parts = response.candidates[0].content.parts
        if parts:
            final_text = "".join(part.text for part in parts if hasattr(part, "text"))
            print("\nFinal Answer from Gemini:\n", final_text)
            return final_text
        else:
            print("\nFinal Answer from Gemini: No response received")
            return "No response received"
    else:
        # No function calls, print answer
        final_text = "".join(part.text for part in parts if hasattr(part, "text"))
        print("\nFinal Answer from Gemini:\n", final_text)
        return final_text


def main():
    MODEL = "gemini-2.0-flash-001"
    model = GenerativeModel(MODEL)
    prompt = "Which numbers are even and which are prime in this list: 4, 7, nine, 19, 23?"
    answer = call_model_loop(model, prompt)
    print(f"\nFinal Response :\n{answer}")

if __name__ == "__main__":
    main()
