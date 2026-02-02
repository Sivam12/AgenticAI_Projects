from google.generativeai import GenerativeModel
from google.generativeai.types.content_types import FunctionDeclaration
from google.generativeai.types.content_types import Tool, ToolConfigType
from google.generativeai import protos

def get_indian_festival_date(festival_name: str) -> str:
    """
    Return the approximate date of an Indian festival.
    """
    festival_dates = {
        "Diwali": "Late October or Early November",
        "Holi": "March",
        "Pongal": "January 14-17",
        "Onam": "August or September",
        "Ganesh Chaturthi": "August or September"
    }
    return festival_dates.get(festival_name, "Date not found")

def get_ipl_team_roster(team_name):
    """
    Return a few prominent players in a given IPL team.
    """
    ipl_rosters = {
        "Mumbai Indians": ["Rohit Sharma", "Jasprit Bumrah", "Suryakumar Yadav"],
        "Chennai Super Kings": ["MS Dhoni", "Ravindra Jadeja", "Ruturaj Gaikwad"],
        "Royal Challengers Bangalore": ["Virat Kohli", "Glenn Maxwell", "Faf du Plessis"]
    }
    return ipl_rosters.get(team_name, "Team not found")

def declare_fun_tool():
    print()
    print("Initializing function tools")
    get_festival_fun = FunctionDeclaration.from_function(get_indian_festival_date)
    get_ipl_fun = FunctionDeclaration.from_function(get_ipl_team_roster)

    indian_context_tool = Tool(function_declarations=[get_festival_fun, get_ipl_fun])

    return indian_context_tool

def none_mode_fun():
    # 1. MODE = NONE
    print("--- MODE = none ---")
    indian_context_tool  = declare_fun_tool()

    prompt = "Tell me something I can use to help understand Indian culture." # A generic prompt
    # prompt = "When is Diwali typically celebrated?  Also, tell me about the Chennai Super Kings."
    print(f"Prompt :{prompt}")
    
    umode = protos.FunctionCallingConfig.Mode.NONE
    uconfig = protos.FunctionCallingConfig(mode=umode)
    
    tool_config_auto = protos.ToolConfig(function_calling_config = uconfig)

    MODEL = "gemini-2.0-flash-001"
    model = GenerativeModel(MODEL)

    response = model.generate_content(prompt, tools=[indian_context_tool], tool_config=tool_config_auto)
    if response.candidates[0].content.parts:
        print("Response Parts:")
        for part in response.candidates[0].content.parts:
            print(part)
        print("\n")
    else:
        print("No response content.\n")


def main():
    none_mode_fun()

if __name__ == "__main__":
    main()
