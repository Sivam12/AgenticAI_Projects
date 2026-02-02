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
def call_model(model, prompt, tools=None):
    print(f"=============={prompt}==============")
    print(f"Entering call_model with prompt: {prompt}, tools: {tools}")
    response = model.generate_content(prompt, tools=tools)
    print(f"Model response: {response}")
    print("Exiting call_model")
    return response

def call_model_loop(model, prompt):
    tools = get_tool_declarations()

    print(f"==============Prompt: {prompt}==============\n")

    response = model.generate_content(prompt, tools=tools)
    print(f"call_model_loop: Response received")

    parts = response.candidates[0].content.parts
    print(f"call_model_loop: Number of parts in response: {len(parts)}")

    for part in parts:
        call = part.function_call
        print(f"\nFunction Call Detected:")
        print(f"  Name: {call.name}")
        arguments = {key: value for key, value in call.args.items()}
        print(f"  Arguments: {arguments}")

def main():
    MODEL = "gemini-2.0-flash-001"
    model = GenerativeModel(MODEL)
    prompt = "Which numbers are even and which are prime in this list: 4, 7, nine, 19, 23?"
    call_model_loop(model, prompt)

if __name__ == "__main__":
    main()
