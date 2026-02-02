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
    GITHUB_MCP_SERVER_URL = os.getenv("GIT_MCPSERVER_URL")
    #print(f'GITHUB_MCP_SERVER_URL: {GITHUB_MCP_SERVER_URL}')
    return GITHUB_MCP_SERVER_URL

async def make_mcp_connection(url: str):
    client = Client(url)
    await client.__aenter__()
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
    payload = json.loads(mcp_tool_response_text)

    details = (
        payload.get("data", {})
               .get("details", [])
    )

    file_list: List[str] = []
    file_patches: List[Tuple[str, Optional[str]]] = []

    for item in details:
        filename = item.get("filename")
        if not filename:
            continue

        patch = item.get("patch")  # may be missing for large diffs
        file_list.append(filename)
        file_patches.append((filename, patch))

    return file_list, file_patches


async def fetch_pr_details(mcp_connection,pr_details):
    print(f'GIT_AGENT: mcp_connection {mcp_connection}"]')
    print(f'GIT_AGENT: pr_details {pr_details}')
    #tools = await mcp_connection.list_tools()

    #GITHUB_GET_A_PULL_REQUEST
    # print("Available tools:")
    # for tool in tools:
    #     print(f"{tool.model_dump_json(indent=4)}")
    
    tool_name = "GITHUB_LIST_PULL_REQUESTS_FILES"
    args = {"owner": "Sivam12", "pull_number": 1, "repo": "issue-tracker"}

    print(f"Invoke tool :'{tool_name}' with args :{args}")
    result = await mcp_connection.call_tool(tool_name, arguments=args)
    print(result.content[0].text)
    print(type(result.content[0].text))
    # json_reply=json.loads(result.content[0].text)
    file_list, patch=extract_pr_files_and_patches(result.content[0].text)
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


    return 'siva',1001



def fetch_file_details(mcp_connection,pr_details):
    return ['a.py','b.py','c.py']

def diff_details(mcp_connection,pr_details):
    return 'hello world'

def git_read_init(v_GitReadAgent: GitReadAgent):
    print('GIT_AGENT: git_read_init')
    print(f'GIT_AGENT: {v_GitReadAgent}')
    v_GitReadAgent["mcp_connection"]=None
    v_GitReadAgent["mcp_server_url"]= get_mcp_server_url()
    v_GitReadAgent["owner"]=None
    v_GitReadAgent["pr_number"]=0
    v_GitReadAgent["file_list"]=[]
    v_GitReadAgent["diff"]=None
    return v_GitReadAgent

async def connect_mcp(v_GitReadAgent: GitReadAgent):
    print('GIT_AGENT: connect_mcp')
    print('GIT_AGENT: connect_mcp successful')

    v_GitReadAgent["mcp_connection"]=await make_mcp_connection(v_GitReadAgent["mcp_server_url"])
    print(f"✅ Connected to MCP")
    return v_GitReadAgent

async def fetch_pr(v_GitReadAgent: GitReadAgent):
    print('GIT_AGENT: fetch_pr')
    owner,pr_number=await fetch_pr_details(v_GitReadAgent["mcp_connection"],v_GitReadAgent["pr_details"])
    v_GitReadAgent["owner"]=owner
    v_GitReadAgent["pr_number"]=pr_number
    return v_GitReadAgent
    
def fetch_files(v_GitReadAgent: GitReadAgent):
    print('GIT_AGENT: fetch_files')
    file_list=fetch_file_details(v_GitReadAgent["mcp_connection"],v_GitReadAgent["pr_details"])
    v_GitReadAgent["file_list"]=file_list
    return v_GitReadAgent

def extract_diffs(v_GitReadAgent: GitReadAgent):
    print('GIT_AGENT: extract_diffs')
    diff=diff_details(v_GitReadAgent["mcp_connection"],v_GitReadAgent["pr_details"])
    v_GitReadAgent["diff"]=diff
    print(f'GIT_AGENT: Final return Value: {v_GitReadAgent}')
    return v_GitReadAgent

def build_git_agent():
    workflow = StateGraph(GitReadAgent)

    workflow.add_node("GIT_READ_INIT_NODE", git_read_init)
    workflow.add_node("CONNECT_MCP_NODE", connect_mcp)
    workflow.add_node("FETCH_PR_NODE", fetch_pr)
    workflow.add_node("FETCH_FILES_NODE", fetch_files)
    workflow.add_node("EXTRACT_DIFFS_NODE", extract_diffs)

    workflow.add_edge(START, "GIT_READ_INIT_NODE")
    workflow.add_edge("GIT_READ_INIT_NODE", "CONNECT_MCP_NODE")
    workflow.add_edge("CONNECT_MCP_NODE", "FETCH_PR_NODE")
    workflow.add_edge("FETCH_PR_NODE", "FETCH_FILES_NODE")
    workflow.add_edge("FETCH_FILES_NODE", "EXTRACT_DIFFS_NODE")
    workflow.add_edge("EXTRACT_DIFFS_NODE", END)

    git_read_agent = workflow.compile()

    save_graph_as_png(git_read_agent, __file__)

    return git_read_agent

git_read_agent = build_git_agent()

if __name__ == "__main__":
    response = git_read_agent.invoke({"pr_details": 'github.com/pr1'})
    print(f"GIT_AGENT:Response :{response}")
