from langgraph.graph import StateGraph, START, END
from lg_utility import save_graph_as_png
from typing import TypedDict,Optional,Any,List, Dict,Tuple
import asyncio
from fastmcp import Client
import os
import json

class GitReadAgent(TypedDict):
     pr_details: str
     mcp_connection: Optional[Any]
     mcp_server_url: str
     owner: str
     pr_number: int
     file_list: list
     diff: str

def get_mcp_server_url():
    print("\n[GIT] get_mcp_server_url")
    GITHUB_MCP_SERVER_URL = os.getenv("GITHUB_MCP_SERVER_URL")
    print(f"  └─ URL: {GITHUB_MCP_SERVER_URL}")
    return GITHUB_MCP_SERVER_URL

async def make_mcp_connection(url: str):
    print("\n[GIT] make_mcp_connection")
    print(f"  └─ URL: {url}")
    client = Client(url)
    await client.__aenter__()
    print(f"  └─ ✓ Connection established")
    return client

def extract_pr_files_and_patches(mcp_tool_response_text: str) -> Tuple[List[str], List[Tuple[str, Optional[str]]]]:
    """
    Extracts ONLY:
      1) file_list: [ "path/to/file1", "path/to/file2", ... ]
      2) file_patches: [ ("path/to/file1", "<patch>"), ("path/to/file2", None), ... ]

    Input must be the raw string you printed:
      result.content[0].text
    (Your MCP response shape: {"successful":true,"data":{"details":[...]} ...})
    """
    print("\n[GIT] extract_pr_files_and_patches")
    print(f"  └─ Parsing response ({len(mcp_tool_response_text)} chars)")
    
    payload = json.loads(mcp_tool_response_text)

    details = (
        payload.get("data", {})
               .get("details", [])
    )

    print(f"  └─ Found {len(details)} file details")

    file_list: List[str] = []
    file_patches: List[Tuple[str, Optional[str]]] = []

    for idx, item in enumerate(details):
        filename = item.get("filename")
        if not filename:
            print(f"     └─ [#{idx}] ✗ Missing filename, skipping")
            continue

        patch = item.get("patch")  # may be missing for large diffs
        file_list.append(filename)
        file_patches.append((filename, patch))
        
        patch_info = "No patch" if patch is None else f"{len(patch)} chars"
        print(f"     └─ [#{idx}] {filename} ({patch_info})")

    print(f"  └─ ✓ Extracted {len(file_list)} files")
    return file_list, file_patches


async def git_mcps_list_tools(mcp_connection):
    print("\n[GIT] git_mcps_list_tools")
    tools = await mcp_connection.list_tools()

    print("Available tools:")
    for tool in tools:
        print(f"{tool.model_dump_json(indent=4)}")

async def fetch_pr_details(mcp_connection,pr_details):
    print("\n[GIT] fetch_pr_details")
    print(f"  └─ PR: {pr_details}")
    
    tool_name = "GITHUB_LIST_PULL_REQUESTS_FILES"
    args = {"owner": "Sivam12", "pull_number": 1, "repo": "issue-tracker"}

    print(f"  └─ Calling MCP tool: {tool_name}")
    print(f"     └─ Args: {args}")
    
    result = await mcp_connection.call_tool(tool_name, arguments=args)
    
    print(f"  └─ Response received ({len(result.content[0].text)} chars)")
    
    file_list, patch = extract_pr_files_and_patches(result.content[0].text)
    
    print(f"  └─ Patch details: {len(patch)} items")
    print(f"  └─ File list: {file_list}")
    return file_list, patch



def fetch_file_details(mcp_connection,pr_details):
    print("\n[GIT] fetch_file_details")
    result = ['a.py','b.py','c.py']
    print(f"  └─ Returning {len(result)} files: {result}")
    return result

def diff_details(mcp_connection,pr_details):
    print("\n[GIT] diff_details")
    result = 'hello world'
    print(f"  └─ Returning diff")
    return result

def git_read_init(v_GitReadAgent: GitReadAgent):
    print('\n[GIT] git_read_init')
    v_GitReadAgent["mcp_connection"]=None
    v_GitReadAgent["mcp_server_url"]= get_mcp_server_url()
    v_GitReadAgent["owner"]=None
    v_GitReadAgent["pr_number"]=0
    v_GitReadAgent["file_list"]=[]
    v_GitReadAgent["diff"]=None
    print(f'  └─ ✓ State initialized')
    return v_GitReadAgent

async def connect_mcp(v_GitReadAgent: GitReadAgent):
    print('\n[GIT] connect_mcp')
    print(f'  └─ Connecting to: {v_GitReadAgent["mcp_server_url"]}')
    v_GitReadAgent["mcp_connection"]=await make_mcp_connection(v_GitReadAgent["mcp_server_url"])
    print(f"  └─ ✓ MCP Connected")
    return v_GitReadAgent

async def fetch_pr(v_GitReadAgent: GitReadAgent):
    print('\n[GIT] fetch_pr')
    file_list, patch = await fetch_pr_details(v_GitReadAgent["mcp_connection"], v_GitReadAgent["pr_details"])
    v_GitReadAgent["file_list"] = file_list
    v_GitReadAgent["diff"] = patch
    print(f'  └─ ✓ PR fetched - files: {file_list}, Patch#: {patch}')
    return v_GitReadAgent
    
def build_git_agent():
    print("\n[GIT] build_git_agent")
    workflow = StateGraph(GitReadAgent)

    workflow.add_node("GIT_READ_INIT_NODE", git_read_init)
    workflow.add_node("CONNECT_MCP_NODE", connect_mcp)
    workflow.add_node("FETCH_PR_NODE", fetch_pr)

    workflow.add_edge(START, "GIT_READ_INIT_NODE")
    workflow.add_edge("GIT_READ_INIT_NODE", "CONNECT_MCP_NODE")
    workflow.add_edge("CONNECT_MCP_NODE", "FETCH_PR_NODE")
    workflow.add_edge("FETCH_PR_NODE", END)

    print("  └─ Compiling workflow...")
    git_read_agent = workflow.compile()

    print(f"  └─ Saving graph visualization...")
    save_graph_as_png(git_read_agent, __file__)
    print("  └─ ✓ Git agent ready")

    return git_read_agent

print("\n[GIT] Initializing git_read_agent...")
git_read_agent = build_git_agent()
print("[GIT] ✓ git_read_agent initialized\n")

if __name__ == "__main__":
    print("\n[GIT] Running as main...")
    response = git_read_agent.invoke({"pr_details": 'github.com/pr1'})
    print(f"\n[GIT] Response: {response}")