from google.generativeai import GenerativeModel
from google.generativeai.types.content_types import FunctionDeclaration
from google.generativeai.types.content_types import Tool

def declare_functions():
    get_location = FunctionDeclaration(
        name="get_location",
        description="Get latitude and longitude for a given location",
        parameters={
            "type": "object",
            "properties": {
                "poi": {"type": "string", "description": "Point of interest (e.g., Infosys Campus)"},
                "street": {"type": "string", "description": "Street or road name"},
                "city": {"type": "string", "description": "City name (e.g., Bengaluru)"},
                "county": {"type": "string", "description": "District name"},
                "state": {"type": "string", "description": "State name (e.g., Karnataka)"},
                "country": {"type": "string", "description": "Country name (India)"},
                "postal_code": {"type": "string", "description": "Pincode"},
            },
        },
    )

    location_tool = Tool(function_declarations=[get_location])
    return location_tool


def main():
    MODEL = "gemini-2.0-flash-001"
    model = GenerativeModel(model_name=MODEL)
    
    location_tool = declare_functions()

    prompt = """
    I want to get the coordinates for the following Indian address:
    Infosys Campus, Electronics City Phase 1, Hosur Road,
    Bengaluru, Karnataka, 560100, India
    """

    response = model.generate_content(prompt, tools=[location_tool])
    print(response.candidates[0].content.parts[0])
    print()


if __name__ == "__main__":
    main()
