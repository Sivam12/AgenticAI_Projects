from google.generativeai import GenerativeModel
from google.generativeai.types.content_types import FunctionDeclaration
from google.generativeai.types.content_types import Tool

def get_product_info(product_name: str) -> dict:
    """Get the stock amount and identifier for a given product"""
    pass

def get_store_location(location: str) -> dict:
    """Get the location of the closest store"""
    pass

def place_order(product: str, address: str) -> dict:
    """Place an order"""
    pass

def declare_functions():
    product_info_decl = FunctionDeclaration.from_function(get_product_info)
    store_location_decl = FunctionDeclaration.from_function(get_store_location)
    place_order_decl = FunctionDeclaration.from_function(place_order)
    
    functions = [product_info_decl, store_location_decl, place_order_decl]
    retail_tool = Tool(function_declarations=functions)
    
    return retail_tool

def main():
    MODEL = "gemini-2.0-flash-001"
    retail_tool = declare_functions()       # Declare available function tools

    # Initialize Gemini model client with tools already attached
    model = GenerativeModel(MODEL, tools=[retail_tool])  

    prompt = "Do you have the book titled 'Let Us C'?"

    # Explicitly pass tools again (overrides/extends default tools set on model)
    response = model.generate_content(prompt, tools=[retail_tool])
    print(f"Response:\n{response.candidates[0].content.parts[0]}")

    # Call without tools (relies only on model’s default behavior)
    response = model.generate_content(prompt)
    print(f"Response:\n{response.candidates[0].content.parts[0]}")

if __name__ == "__main__":
    main()
