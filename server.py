from fastmcp import FastMCP
from tools import pucit_tools

mcp = FastMCP("cgpa")

for fn in pucit_tools:
    mcp.tool(fn)

if __name__=="__main__":
    mcp.run(transport="http",host="127.0.0.1",port=8000)

    