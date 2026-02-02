from google.generativeai import GenerativeModel
from google.generativeai.types.content_types import FunctionDeclaration
from google.generativeai.types.content_types import Tool
import requests

def get_exchange_rate(currency_date: str, currency_from: str, currency_to: str) -> str:
    """
    Fetches the exchange rate between two currencies for a given date using the Frankfurter API.

    Args:
        currency_date (str): The date for which the exchange rate is requested,
            in the format 'YYYY-MM-DD'. Use 'latest' for the most recent rates.
        currency_from (str): The source currency code (e.g., 'USD').
        currency_to (str): The target currency code (e.g., 'EUR').

    Returns:
        str | dict: The API response text if the request is successful.
            If an error occurs, returns a dictionary with the error message:
            {
                "error": "<error_message>"
            }

    Raises:
        requests.exceptions.RequestException: If the request fails due to network
            issues or invalid API response.
        Exception: For any unexpected errors not covered by RequestException.

    Example:
        >>> get_exchange_rate("2022-09-01", "USD", "INR")
        '{"amount":1.0,"base":"USD","date":"2022-09-01","rates":{"INR":79.5}}'
    """
    try:
        url = f"https://api.frankfurter.app/{currency_date}"
        params = {"from": currency_from, "to": currency_to}
        
        print(f"\tRequesting URL: {url} with params: {params}\n")
        
        api_response = requests.get(url, params=params)
        api_response.raise_for_status()
        
        return api_response.text
    
    except requests.exceptions.RequestException as e:
        error_message = f"Error fetching exchange rate: {e}"
        print(error_message)
        return {"error": error_message}
    
    except Exception as e:
        error_message = f"An unexpected error occurred: {e}"
        print(error_message)
        return {"error": error_message}

def declare_fun_tools():
    print("Initializing function tools")
    exchange_rate_fun = FunctionDeclaration.from_function(get_exchange_rate)
    exchange_rate_tool = Tool(function_declarations=[exchange_rate_fun])

    return exchange_rate_tool

def execute_function(function_name, arguments):
    print(f"In execute_function...")
    if function_name == "get_exchange_rate":
        try:
            currency_date = arguments.get("currency_date")
            currency_from = arguments.get("currency_from")
            currency_to = arguments.get("currency_to")
            result = get_exchange_rate(currency_date, currency_from, currency_to)
            print(f"\nresult :{result}\n")
            return result
        except (ValueError, TypeError) as e:
            raise
    else:
        raise ValueError("Unknown function called.")


def call_model_and_execute_tools(model, tools, prompt):
    print(f"Prompt:\n{prompt}")
    response = model.generate_content(prompt, tools=tools)
    
    # function_call = extract_function_call(response)
    function_call = None
    if (response.candidates and \
        response.candidates[0].content.parts and \
        response.candidates[0].content.parts[0].function_call):
        function_call = response.candidates[0].content.parts[0].function_call

    if function_call:
        function_name = function_call.name
        arguments = {key: value for key, value in function_call.args.items()}

        print()
        print("Got response from LLM:")
        print(f"    Function to call: '{function_name}'")
        print("    Arguments:", arguments)
        print()

        print(f"Calling function: {function_name}...")
        try:
            return execute_function(function_name, arguments)
        except (ValueError, TypeError) as e:
            error_message = f"Error: {e}"
            print(error_message)
            return error_message

def main():
    MODEL = "gemini-2.0-flash-001"
    model = GenerativeModel(MODEL)
    
    tool = declare_fun_tools()

    prompt = """What is the exchange rate from Indian Rupees to US Dollars on 2024-08-20? 
    How much is 10000 Indian Rupees worth in US Dollars?"""
    
    final_response = call_model_and_execute_tools(model, tool, prompt)
    print()
    print(f"Final response:...\n\t{final_response}")
    print()

if __name__ == "__main__":
    main()