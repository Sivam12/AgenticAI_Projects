from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import asyncio

# Math Server Parameters
server_params = StdioServerParameters(
    command="python",
    args=["05-mcps-stdio.py"],
    env=None,
)

async def main():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            response = await session.list_prompts()
            print("Prompts")
            for prompt in response.prompts:
                print(prompt)

            response = await session.list_resources()
            print("Resources")
            for resource in response.resources:
                print(resource)

            response = await session.list_resource_templates()
            print("Resource Templates")
            for resource_template in response.resourceTemplates:
                print(resource_template)

            response = await session.list_tools()
            print("Tools")
            for tool in response.tools:
                print(tool)

            args = {"question": "what is 2+2"}
            prompt = await session.get_prompt("example_prompt", arguments=args)
            print(prompt.messages[0].content.text)

            content, mime_type = await session.read_resource("greeting://Alice")
            print(mime_type[1][0].text)

            args = {"a": 2, "b": 2}
            result = await session.call_tool("add_numbers", arguments=args)
            print(result.content[0].text)

if __name__ == "__main__":
    asyncio.run(main())