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


def post_question(chat, prompt):
    print()
    whereami(f"Prompt: {prompt}")
    
    response = chat.send_message(prompt)
    
    return response.candidates[0].content.parts[0]

def send_reponse_by_function(chat, response, function_name):
    function_response = protos.FunctionResponse(
        name=function_name,
        response=response
    )
    
    response = chat.send_message(
        protos.Part(function_response=function_response)
    )
    whereami()
    return response

def main():
    MODEL = "gemini-2.0-flash-001"
    
    chat = init_chat(MODEL)
    
    prompt = """Do you have the book titled 'Let Us C' available at your Outer Ring Road, Marathahalli branch? 
    I’d like to visit and also have it shipped to 6th Cross, Ambedkar Nagar, Sarjapur Road, Bengaluru - 560035, India. 
    If the stock is available, Place the order to above address."""

    response = chat.send_message(prompt)
    
    for part in response.candidates[0].content.parts:
        print(f"Tool :\n{part}")

    # Tool1 Response - Stock details
    stock_details = {"sku": "BPB-CBOOKS-KDP", "in_stock": "yes"}
    tool_response = protos.FunctionResponse(name="get_product_info", response=stock_details)
    stock_reply = protos.Part(function_response=tool_response)

    # Tool2 Response - Location details
    store_location = {"store": "77/1, Marathahalli, Bengaluru, 560103, IND"}
    tool_response = protos.FunctionResponse(name="get_store_location", response=store_location)
    location_reply = protos.Part(function_response=tool_response)
   
    print("Responding Stock and Location details...")
    response = chat.send_message([stock_reply, location_reply])

    print("Got the response...")
    for part in response.candidates[0].content.parts:
        print(f"Tool :\n{part}")

    order_response = {"payment_status": "paid", "order_number": 12345, "est_arrival": "2 days"}
    tool_response = protos.FunctionResponse(name="place_order", response=order_response )
    order_reply = protos.Part(function_response=tool_response)

    print("Placing Order...")
    response = chat.send_message(order_reply)
    
    print(response.text)
    
if __name__ == "__main__":
    main()
    
