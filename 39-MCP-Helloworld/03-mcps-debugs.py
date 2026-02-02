from mcp.server.fastmcp import FastMCP
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("MCPHelloWorld")

mcp = FastMCP(name="Math", host="127.0.0.1", port=3333)

@mcp.tool()
def add_numbers(a: int, b: int) -> int:
    """Addition of 2 numbers"""
    print(f"values of a & b are {a}, {b}")
    return int(a + b)

if __name__ == "__main__":
    mcp.run(transport='streamable-http')
    