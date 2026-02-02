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
    print("GIT_AGENT: get_mcp_server_url - start")
    GITHUB_MCP_SERVER_URL = os.getenv("GIT_MCPSERVER_URL")
    print(f"GIT_AGENT: get_mcp_server_url - env GIT_MCPSERVER_URL: {GITHUB_MCP_SERVER_URL}")
    print("GIT_AGENT: get_mcp_server_url - end")
    return GITHUB_MCP_SERVER_URL

async def make_mcp_connection(url: str):
    print("GIT_AGENT: make_mcp_connection - start")
    print(f"GIT_AGENT: make_mcp_connection - url: {url}")
    client = Client(url)
    print(f"GIT_AGENT: make_mcp_connection - client created: {client}")
    await client.__aenter__()
    print("GIT_AGENT: make_mcp_connection - __aenter__ completed")
    print("GIT_AGENT: make_mcp_connection - end")
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
    print("GIT_AGENT: extract_pr_files_and_patches - start")
    print(f"GIT_AGENT: extract_pr_files_and_patches - input type: {type(mcp_tool_response_text)}")
    try:
        print(f"GIT_AGENT: extract_pr_files_and_patches - input length: {len(mcp_tool_response_text)}")
        print(f"GIT_AGENT: extract_pr_files_and_patches - input preview (first 200 chars): {mcp_tool_response_text[:200]}")
    except Exception as e:
        print(f"GIT_AGENT: extract_pr_files_and_patches - unable to preview input. err: {e}")

    payload = json.loads(mcp_tool_response_text)

    details = (
        payload.get("data", {})
               .get("details", [])
    )

    print(f"GIT_AGENT: extract_pr_files_and_patches - payload keys: {list(payload.keys())}")
    print(f"GIT_AGENT: extract_pr_files_and_patches - details type: {type(details)}")
    try:
        print(f"GIT_AGENT: extract_pr_files_and_patches - details count: {len(details)}")
    except Exception as e:
        print(f"GIT_AGENT: extract_pr_files_and_patches - unable to get details count. err: {e}")

    file_list: List[str] = []
    file_patches: List[Tuple[str, Optional[str]]] = []

    for idx, item in enumerate(details):
        filename = item.get("filename")
        if not filename:
            print(f"GIT_AGENT: extract_pr_files_and_patches - details[{idx}] missing filename, skipping")
            continue

        patch = item.get("patch")  # may be missing for large diffs
        file_list.append(filename)
        file_patches.append((filename, patch))

        patch_status = "None" if patch is None else f"present(len={len(patch)})"
        print(f"GIT_AGENT: extract_pr_files_and_patches - details[{idx}] filename: {filename}, patch: {patch_status}")

    print(f"GIT_AGENT: extract_pr_files_and_patches - extracted file_count: {len(file_list)}")
    print("GIT_AGENT: extract_pr_files_and_patches - end")
    return file_list, file_patches


async def fetch_pr_details(mcp_connection,pr_details):
    print("GIT_AGENT: fetch_pr_details - start")
    print(f'GIT_AGENT: mcp_connection {mcp_connection}"]')
    print(f'GIT_AGENT: pr_details {pr_details}')
    print(f"GIT_AGENT: fetch_pr_details - mcp_connection type: {type(mcp_connection)}")
    print(f"GIT_AGENT: fetch_pr_details - pr_details type: {type(pr_details)}")

    #tools = await mcp_connection.list_tools()

    #GITHUB_GET_A_PULL_REQUEST
    # print("Available tools:")
    # for tool in tools:
    #     print(f"{tool.model_dump_json(indent=4)}")
    
    tool_name = "GITHUB_LIST_PULL_REQUESTS_FILES"
    args = {"owner": "Sivam12", "pull_number": 1, "repo": "issue-tracker"}

    print(f"GIT_AGENT: fetch_pr_details - Invoke tool :'{tool_name}' with args :{args}")
    result = await mcp_connection.call_tool(tool_name, arguments=args)
    print(f"GIT_AGENT: fetch_pr_details - MCP tool call completed. result type: {type(result)}")

    try:
        print(f"GIT_AGENT: fetch_pr_details - result.content type: {type(result.content)}")
        print(f"GIT_AGENT: fetch_pr_details - result.content length: {len(result.content)}")
        print(f"GIT_AGENT: fetch_pr_details - result.content[0] type: {type(result.content[0])}")
        print(f"GIT_AGENT: fetch_pr_details - result.content[0].text type: {type(result.content[0].text)}")
        print(f"GIT_AGENT: fetch_pr_details - result.content[0].text preview (first 200 chars): {result.content[0].text[:200]}")
    except Exception as e:
        print(f"GIT_AGENT: fetch_pr_details - unable to inspect result.content. err: {e}")

    #print(result.content[0].text)
    #print(type(result.content[0].text))
    # json_reply=json.loads(result.content[0].text)
    print("GIT_AGENT: fetch_pr_details - extracting files & patches from MCP response")
    file_list, patch=extract_pr_files_and_patches(result.content[0].text)
    print(f"GIT_AGENT: fetch_pr_details - patchdetails count: {len(patch)}")
    print(f"GIT_AGENT: fetch_pr_details - filelist count: {len(file_list)}")
    print(f"patchdetails :{patch}")
    print(f"filelist :{file_list}")
    #print(json.dumps(json_reply,indent=4,sort_keys=True))
    #print(json_reply["data"]["details"])
    #print(json_reply["data"])
    #print(json.dumps(json_reply["data"]))
    # tool_name = "add_numbers"
    # args = {"a": 6, "b": 10}
    # print(f"Invoke tool :'{tool_name}' with args :{args}")
    # result = await session.call_tool(tool_name, arguments=args)
    # print(result.content[0].text)
    # print()

    print("GIT_AGENT: fetch_pr_details - end")
    return file_list,patch



def fetch_file_details(mcp_connection,pr_details):
    print("GIT_AGENT: fetch_file_details - start")
    print(f"GIT_AGENT: fetch_file_details - mcp_connection: {mcp_connection}")
    print(f"GIT_AGENT: fetch_file_details - pr_details: {pr_details}")
    result = ['a.py','b.py','c.py']
    print(f"GIT_AGENT: fetch_file_details - returning file_list: {result}")
    print("GIT_AGENT: fetch_file_details - end")
    return result

def diff_details(mcp_connection,pr_details):
    print("GIT_AGENT: diff_details - start")
    print(f"GIT_AGENT: diff_details - mcp_connection: {mcp_connection}")
    print(f"GIT_AGENT: diff_details - pr_details: {pr_details}")
    result = 'hello world'
    print(f"GIT_AGENT: diff_details - returning diff preview: {result[:200]}")
    print("GIT_AGENT: diff_details - end")
    return result

def git_read_init(v_GitReadAgent: GitReadAgent):
    print('GIT_AGENT: git_read_init - start')
    print(f'GIT_AGENT: git_read_init - input state: {v_GitReadAgent}')
    v_GitReadAgent["mcp_connection"]=None
    v_GitReadAgent["mcp_server_url"]= get_mcp_server_url()
    v_GitReadAgent["owner"]=None
    v_GitReadAgent["pr_number"]=0
    v_GitReadAgent["file_list"]=[]
    v_GitReadAgent["diff"]=None
    print(f'GIT_AGENT: git_read_init - output state: {v_GitReadAgent}')
    print('GIT_AGENT: git_read_init - end')
    return v_GitReadAgent

async def connect_mcp(v_GitReadAgent: GitReadAgent):
    print('GIT_AGENT: connect_mcp - start')
    print(f'GIT_AGENT: connect_mcp - current state: {v_GitReadAgent}')
    print('GIT_AGENT: connect_mcp successful')

    print(f'GIT_AGENT: connect_mcp - mcp_server_url: {v_GitReadAgent["mcp_server_url"]}')
    v_GitReadAgent["mcp_connection"]=await make_mcp_connection(v_GitReadAgent["mcp_server_url"])
    print(f"✅ Connected to MCP")
    print(f'GIT_AGENT: connect_mcp - mcp_connection: {v_GitReadAgent["mcp_connection"]}')
    print(f'GIT_AGENT: connect_mcp - end state: {v_GitReadAgent}')
    print('GIT_AGENT: connect_mcp - end')
    return v_GitReadAgent

async def fetch_pr(v_GitReadAgent: GitReadAgent):
    print('GIT_AGENT: fetch_pr - start')
    print(f'GIT_AGENT: fetch_pr - input state: {v_GitReadAgent}')
    file_list,patch=await fetch_pr_details(v_GitReadAgent["mcp_connection"],v_GitReadAgent["pr_details"])
    v_GitReadAgent["file_list"]=file_list
    v_GitReadAgent["patch"]=patch
    return v_GitReadAgent
    
def build_git_agent():
    print("GIT_AGENT: build_git_agent - start")
    workflow = StateGraph(GitReadAgent)

    workflow.add_node("GIT_READ_INIT_NODE", git_read_init)
    workflow.add_node("CONNECT_MCP_NODE", connect_mcp)
    workflow.add_node("FETCH_PR_NODE", fetch_pr)
    #workflow.add_node("FETCH_FILES_NODE", fetch_files)
    #workflow.add_node("EXTRACT_DIFFS_NODE", extract_diffs)

    workflow.add_edge(START, "GIT_READ_INIT_NODE")
    workflow.add_edge("GIT_READ_INIT_NODE", "CONNECT_MCP_NODE")
    workflow.add_edge("CONNECT_MCP_NODE", "FETCH_PR_NODE")
    workflow.add_edge("FETCH_PR_NODE", END)
    #workflow.add_edge("FETCH_FILES_NODE", "EXTRACT_DIFFS_NODE")
    #workflow.add_edge("EXTRACT_DIFFS_NODE", END)

    print("GIT_AGENT: build_git_agent - compiling workflow")
    git_read_agent = workflow.compile()
    print("GIT_AGENT: build_git_agent - compile complete")

    print(f"GIT_AGENT: build_git_agent - saving graph png using file: {__file__}")
    save_graph_as_png(git_read_agent, __file__)
    print("GIT_AGENT: build_git_agent - graph png saved")

    print("GIT_AGENT: build_git_agent - end")
    return git_read_agent

print("GIT_AGENT: module import - initializing git_read_agent")
git_read_agent = build_git_agent()
print("GIT_AGENT: module import - git_read_agent initialized")

if __name__ == "__main__":
    print("GIT_AGENT: __main__ - start")
    response = git_read_agent.invoke({"pr_details": 'github.com/pr1'})
    print(f"GIT_AGENT:Response :{response}")
    print("GIT_AGENT: __main__ - end")
