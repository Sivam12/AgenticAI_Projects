from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Math")

# Prompts
@mcp.prompt()
def example_prompt(question: str) -> str:
    """Example prompt description"""
    return f"""
    You are a math assistant. Answer the question.
    Question: {question}
    """

@mcp.prompt()
def system_prompt() -> str:
    """System prompt description"""
    return """
    You are an AI assistant use the tools if needed.
    """

# Resources
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"

@mcp.resource("config://app")
def get_config() -> str:
    """Static configuration data"""
    return "App configuration here"

@mcp.tool()
def add_numbers(a: int, b: int) -> int:
    """Addition of 2 numbers"""
    print(f"values of a & b are {a}, {b}")
    return int(a + b)

@mcp.tool()
def multiply_numbers(a: int, b: int) -> int:
    """Multipllication two numbers"""
    return int(a * b)

if __name__ == "__main__":
    mcp.run()
    