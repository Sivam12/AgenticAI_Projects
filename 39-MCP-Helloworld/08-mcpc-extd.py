from mcp.client.streamable_http import streamablehttp_client
from mcp import ClientSession
import asyncio

 
async def main():
    SERVER_URL = "http://127.0.0.1:3333/mcp/"

    async with streamablehttp_client(SERVER_URL) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()

            response = await session.list_prompts()
            print("Prompts")
            for prompt in response.prompts:
                print(prompt)
            print()
            
            response = await session.list_resources()
            print("Resources")
            for resource in response.resources:
                print(resource)
            print()

            response = await session.list_resource_templates()
            print("Resource Templates")
            for resource_template in response.resourceTemplates:
                print(resource_template)
            print()

            response = await session.list_tools()
            print("Tools")
            for tool in response.tools:
                print(tool)
            print()

            prompt_name = "example_prompt"
            args = {"question": "what is 6 + 10"}
            print(f"Get Prompt of name :'{prompt_name}' with question :{args}")
            prompt = await session.get_prompt(prompt_name, arguments=args)
            print(prompt.messages[0].content.text)
            print()

            resource_name = "greeting"
            args = "PromptlyAI"
            print(f"Get Resource of type :'{resource_name}' with args :{args}")
            content, mime_type = await session.read_resource(f"{resource_name}://{args}")
            print(mime_type[1][0].text)
            print()

            tool_name = "add_numbers"
            args = {"a": 6, "b": 10}
            print(f"Invoke tool :'{tool_name}' with args :{args}")
            result = await session.call_tool(tool_name, arguments=args)
            print(result.content[0].text)
            print()

if __name__ == "__main__":
    asyncio.run(main())