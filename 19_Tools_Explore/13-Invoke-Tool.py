from pdbwhereami import whereami
from google.generativeai import GenerativeModel
from google.generativeai.types.content_types import FunctionDeclaration
from google.generativeai.types.content_types import Tool
from google.generativeai import protos

def get_product_info(product_name: str) -> dict:
    """Get the stock amount and identifier for a given product"""
    return {"sku": "BPB-CBOOKS-KDP", "in_stock": "yes"}
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
    model = GenerativeModel(model, tools=[retail_tool])

    chat = model.start_chat()                      # Create persistent chat session
    return chat

def main():
    MODEL = "gemini-2.0-flash-001"
    
    chat = init_chat(MODEL)   # Initialize chat with model and registered tools
    
    # === User Prompt ===
    prompt = "Do you have the book titled 'Let Us C'?"
    response = chat.send_message(prompt)   # Send first query
    print(f"==================={prompt}====================")
    print(f"response :\n{response.candidates[0].content.parts[0]}")

    # == Tool Invocation ==
    function_call = response.candidates[0].content.parts[0].function_call
    args = {key: value for key, value in function_call.args.items()}  # Extract arguments
    
    print(f"function_call :{function_call}")
    print(f"args :{args}")
    
    stock_details = get_product_info(args['product_name'])            # Call backend function
    
    # Wrap function output in proper FunctionResponse
    tool_response = protos.FunctionResponse(
        name="get_product_info",
        response=stock_details
    )
    reply = protos.Part(function_response=tool_response)
   
    # === Send tool response back to model ===
    response = chat.send_message(reply)

    # === Final Model Reply ===
    print("Final response :")    
    print(response.text)
    print()

if __name__ == "__main__":
    main()
    
