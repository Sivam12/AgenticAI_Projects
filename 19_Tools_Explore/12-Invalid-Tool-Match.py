from pdbwhereami import whereami
from google.generativeai import GenerativeModel
from google.generativeai.types.content_types import FunctionDeclaration
from google.generativeai.types.content_types import Tool
from google.generativeai import protos

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

def init_chat(model):
    retail_tool = declare_functions()              # Register function tool(s)
    # model = GenerativeModel(model, tools=[retail_tool])
    model = GenerativeModel(model)

    chat = model.start_chat()                      # Create persistent chat session
    return chat

def main():
    MODEL = "gemini-2.0-flash-001"
    
    chat = init_chat(MODEL)                        # Initialize model with tools and chat
    
    prompt = "What is the temparature in Kadapa?"
    response = chat.send_message(prompt)           # Send query to model
    print(response)
    print(f"response :\n{response.candidates[0].content.parts[0]}")  # Print first candidate response
    

if __name__ == "__main__":
    main()
    
    

