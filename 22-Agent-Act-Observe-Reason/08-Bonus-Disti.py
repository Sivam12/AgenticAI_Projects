from google.generativeai import GenerativeModel
from google.generativeai.types.content_types import FunctionDeclaration
from google.generativeai.types.content_types import Tool
from google.generativeai import protos
import bonus_prompts as bp

def collect_financial_data():
    """
    Collects the company's dummy financial data for demonstration purposes.

    Returns:
        dict: A dictionary containing mock financial information with the following keys:
            - revenue (int): Total company revenue.
            - expenditure (int): Total company expenditure.
            - investment (int): Amount invested.
            - credits (int): Outstanding credits available.
            - outstanding (int): Pending financial obligations.
    """
    return {
        "revenue": 1000000,
        "expenditure": 600000,
        "investment": 100000,
        "credits": 50000,
        "outstanding": 20000,
    }


def collect_employee_details():
    """
    Collects dummy employee details for demonstration purposes.

    Returns:
        list[dict]: A list of employee records, where each record contains:
            - id (str): Unique employee identifier.
            - name (str): Employee's full name.
            - age (int): Employee's age in years.
            - rating (float): Employee's performance rating on a scale of 0–5.
            - tenure (int): Number of months the employee has been with the company.
            - etype (str): Employment type, either "fte" (full-time employee) or "contractor".
    """
    return [
        {"id": "E01", "name": "Priya Sharma", "age": 29, "rating": 4.5, "tenure": 18, "etype": "fte"},
        {"id": "E02", "name": "Rahul Verma", "age": 35, "rating": 2.8, "tenure": 25, "etype": "fte"},
        {"id": "E03", "name": "Anjali Kapoor", "age": 42, "rating": 4.2, "tenure": 22, "etype": "fte"},
        {"id": "E04", "name": "Amit Patel", "age": 27, "rating": 3.5, "tenure": 9, "etype": "contractor"},
        {"id": "E05", "name": "Sneha Nair", "age": 31, "rating": 4.8, "tenure": 4, "etype": "fte"}
    ]

def declare_tools() -> Tool:
    """ Declaring tools"""

    finance_func = FunctionDeclaration.from_function(collect_financial_data)
    emp_func = FunctionDeclaration.from_function(collect_employee_details)

    ftools = [finance_func, emp_func]
    agent_tool = Tool(function_declarations=ftools)

    return agent_tool

def process_function_call(part):
    call = part.function_call
    func_name = call.name
    args = {key: value for key, value in call.args.items()}

    print(f"Invoking '{func_name}..{args}'")

    if func_name == "collect_financial_data":
        result = collect_financial_data()
    elif func_name == "collect_employee_details":
        result = collect_employee_details()
    else:
        result = None

    fresponse = {"result" : result}
    tool_response = protos.FunctionResponse(
        name=func_name,
        response=fresponse
    )
    reply = protos.Part(function_response=tool_response)

    print()
    return reply

def call_model_loop(chat, prompt):

    # Interate till LLM asks invoke functions
    while True:
        print('{:*^50}'.format('prompt'))
        print(f"{prompt}\n")

        response = chat.send_message(prompt)
        print(f"Got reponse from LLM...")
        # print(response)
        # print()
        parts = response.candidates[0].content.parts
    
        has_function_call = False

        tool_response = []
        # Interate till all functions invoked
        for i, part in enumerate(parts, start=1):
            if part.function_call.name:
                has_function_call = True
                f_response = process_function_call(part)
                tool_response.append(f_response) 

        if not has_function_call and parts:
            print(f"LLM: NO function to Invoke...")
            return response
        elif not parts:
            print(f"call_model_loop: No parts in response")
            return "No response received"
        else:
            print(f"\nGoing back to LLM...\n")

        prompt = tool_response
    
    
def main():
    MODEL = "gemini-2.0-flash-001"
    agent_tools = declare_tools()

    model = GenerativeModel(MODEL, tools=agent_tools)
    chat = model.start_chat()

    prompt = bp.simple_prompt
    prompt = bp.detailed_prompt
    prompt = bp.structured_input
    prompt = bp.structured_input_ouput
    prompt = bp.no_contractors
    prompt = bp.ftes_and_tenure
    prompt = bp.rating_fte_only
    prompt = bp.more_instructions
    prompt = bp.final_prompt

    response = call_model_loop(chat, prompt)
    print(f"Final response :{response.text}")

if __name__ == "__main__":
    main()
