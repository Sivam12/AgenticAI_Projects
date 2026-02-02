from google.generativeai import GenerativeModel
from google.generativeai.types.content_types import FunctionDeclaration
from google.generativeai.types.content_types import Tool

def get_destination_params(destination: str, mode_of_transportation: str, departure_time: str) -> str:
    """
    Get directions to a destination with transportation mode and departure time.
    
    Args:
        destination (str): The destination to get directions to
        mode_of_transportation (str): Mode of transport (car, bus, train, flight, walk)
        departure_time (str): When the user will leave for the destination
        
    Returns:
        str: Directions with transportation and timing details
    """
    
    # Return concise directions
    return f"To {destination} by {mode_of_transportation}: at {departure_time}"


def declare_fun_tool():
    print()
    print("Initializing function tools")

    get_dest_fun = FunctionDeclaration.from_function(get_destination_params)
    destination_tool = Tool(function_declarations=[get_dest_fun])

    return destination_tool


def main():
    destination_tool  = declare_fun_tool()

    MODEL = "gemini-2.0-flash-001"
    model = GenerativeModel(MODEL)
    
    prompt = "I'd like to travel to Bhuvaneswar, Odisha by train and leave at 9:00 am on 30 July 2025"
    prompt = "I'd like to travel to Tirupati, Andhra by Bus and leave at 9:00 am on 30 July 2025"
    print(f"#### Prompt: {prompt}\n")
    
    response = model.generate_content(prompt, tools=[destination_tool])
    print(f"Response:\n{response.candidates[0].content.parts[0]}")
    
    print()

if __name__ == "__main__":
    main()
