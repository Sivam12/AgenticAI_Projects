from google.generativeai import GenerativeModel
from google.generativeai.types.content_types import FunctionDeclaration
from google.generativeai.types.content_types import Tool

def get_destination(destination: str) -> str:
    """
    Get directions to a destination.
    
    Args:
        destination (str): The destination to get directions to
        
    Returns:
        str: Directions or route information as a string
    """
    
    return f"To {destination}: NH-7 from Delhi or via Haridwar"


def declare_fun_tool():
    print()
    print("Initializing function tools")

    get_dest_fun = FunctionDeclaration.from_function(get_destination)
    destination_tool = Tool(function_declarations=[get_dest_fun])
    
    return destination_tool

def main():
    destination_tool  = declare_fun_tool()

    MODEL = "gemini-2.0-flash-001"
    model = GenerativeModel(MODEL)
    prompt = "I'd like to travel to Uttarakhand"
    print(f"#### Prompt: {prompt}\n")

    response = model.generate_content(prompt, tools=[destination_tool])
    print(f"Response:\n{response.candidates[0].content.parts[0]}")
    
    print()

if __name__ == "__main__":
    main()
