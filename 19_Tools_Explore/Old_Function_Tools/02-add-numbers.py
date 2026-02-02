from pdbwhereami import whereami
from google.generativeai import GenerativeModel
from google.generativeai.types.content_types import FunctionDeclaration
from google.generativeai.types.content_types import Tool

def declare_tools():
    add_numbers_func = FunctionDeclaration(
        name="add_numbers",
        description="Adds two numbers together.",
        parameters={
            "type": "object",
            "properties": {
                "num1": {
                    "type": "number",
                    "description": "The first number."
                },
                "num2": {
                    "type": "number",
                    "description": "The second number."
                }
            },
            "required": ["num1", "num2"]
        },
    )


    add_numbers_tool = Tool(
        function_declarations=[add_numbers_func],
    )
    
    return add_numbers_tool

def add_numbers(num1, num2):
    """Adds two numbers."""
    result = num1 + num2
    print(f"Calling add_numbers({num1}, {num2}) = {result}")
    return result


def call_model_and_execute_tools(model, tool, prompt):
    response = model.generate_content(
        prompt,
        tools=[tool],
    )

    if not response.candidates[0].content.parts[0].function_call:
        return response
        
    function_call = response.candidates[0].content.parts[0].function_call
    function_name = function_call.name
    arguments = {key: value for key, value in function_call.args.items()}
    
    whereami(f"function_call :...\n{function_call}")
    whereami(f"function_name :{function_name}")
    whereami(f"arguments     :{arguments}")

    if function_name != "add_numbers":
        return "Unknown function called."

    num1 = float(arguments["num1"])
    num2 = float(arguments["num2"])
    result = add_numbers(num1, num2)

    followup_prompt = f"The result of add_numbers is: {result}, provide me brief summary"
    followup_response = model.generate_content(followup_prompt)
    print("Model's final response:", followup_response.candidates[0].content.parts[0].text)
    return followup_response
 

def main():  
    MODEL = "gemini-2.0-flash-001"
    model = GenerativeModel(MODEL)
    tool = declare_tools()
    
    prompt1 = "What is 5 plus 10?"
    final_response1 = call_model_and_execute_tools(model, tool, prompt1)
    print(final_response1.text)

if __name__ == "__main__":
    main()
    