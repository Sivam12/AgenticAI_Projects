from google.generativeai import GenerativeModel
from google.generativeai.types.content_types import FunctionDeclaration
from google.generativeai.types.content_types import Tool

def get_location_coordinates(locations: list) -> str:
    """
    Get coordinates of multiple locations.
    
    Args:
        locations (list): A list of location objects, each containing:
            - point_of_interest (str): Name or type of point of interest
            - city (str): City name
            - country (str): Country name
            
    Returns:
        str: Formatted string with coordinates for all locations
    """
    
    result = []
    
    for location in locations:
        poi = location['point_of_interest']
        city = location['city']
        country = location['country']
        
        # Mock coordinates - in real implementation would call geocoding API
        coordinates = f"({poi} in {city}, {country}: lat/lng coordinates)"
        result.append(coordinates)
    
    return ", ".join(result)

def declare_fun_tool():
    print()
    print("Initializing function tools")

    get_dest_fun = FunctionDeclaration.from_function(get_location_coordinates)
    geocoding_tool = Tool(function_declarations=[get_dest_fun],)

    return geocoding_tool

def main():
    destination_tool  = declare_fun_tool()

    MODEL = "gemini-2.0-flash-001"
    model = GenerativeModel(MODEL)

    prompt = """
        I'd like to get the coordinates for
        the Red Fort in Delhi,
        the Gateway of India in Mumbai,
        Vidhana Soudha in Bengaluru,
        and the Golden Temple in Amritsar.
    """
    
    print(f"#### Prompt: {prompt}\n")
    response = model.generate_content(prompt, tools=[destination_tool])
    print(f"Response:\n{response.candidates[0].content.parts[0]}")
    
    print()

if __name__ == "__main__":
    main()
