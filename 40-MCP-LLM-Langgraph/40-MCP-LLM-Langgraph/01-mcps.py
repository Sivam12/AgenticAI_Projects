from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name="Math", host="127.0.0.1", port=3333)

@mcp.prompt()
def system_prompt() -> str: 
    """System prompt description"""
    return """
    You are an AI assistant use the tools if needed.
    """

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
    mcp.run(transport='streamable-http')
    