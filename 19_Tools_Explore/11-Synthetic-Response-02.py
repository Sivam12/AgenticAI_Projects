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
    retail_tool = declare_functions()              # Build tool with function declarations
    model = GenerativeModel(model, tools=[retail_tool])  

    chat = model.start_chat()                      # Create a stateful chat session
    # return model
    return chat

def main():
    MODEL = "gemini-2.0-flash-001"
    
    model = init_chat(MODEL)
    
    prompt = "Do you have the book titled 'Let Us C'?"
    response = model.generate_content(prompt)
    print(f"==================={prompt}====================")
    print(f"response :\n{response.candidates[0].content.parts[0]}")

    stock_details = {"sku": "BPB-CBOOKS-KDP", "in_stock": "yes"}
    tool_response = protos.FunctionResponse(
        name="get_product_info",
        response=stock_details
    )
    reply = protos.Part(function_response=tool_response)
   
    response = model.generate_content(reply)

    print("Final response :")    
    print(response)
    print(response.text)
    
    print()

if __name__ == "__main__":
    # print("TODO")
    # exit(1)
    main()
    
