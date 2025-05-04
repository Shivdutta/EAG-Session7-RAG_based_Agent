from fastapi import FastAPI, HTTPException
import inspect
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from mcp_server import mcp

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your extension's origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model for the incoming payload
class PageContent(BaseModel):
    url: str
    title: str
    text: str
    
@app.post("/add_to_index")
async def add_to_index(payload: PageContent):
    try:
        print("Processing HTML content...")

        print("Received payload url:", payload.url)
        print("Received payload title:", payload.title)
        print("Received payload text:", payload.text)

        # Prepare arguments to call the 'process_documents' MCP tool
        arguments = {
            "url": payload.url,
            "title": payload.title,
            "text": payload.text
        }

        # Check if the 'process_documents' tool is available
        tools = await mcp.list_tools()  # Await the coroutine to get the tools
        process_documents_tool = next((tool for tool in tools if tool.name == 'process_html'), None)

        if process_documents_tool is None:
            raise HTTPException(status_code=404, detail="Tool 'process_html' not found")

        # Call the MCP tool
        result = await mcp.call_tool('process_html', arguments)

        # Assuming 'result' contains the chunks or some response from the tool
        return {
            "status": "success",
            "message": "HTML Document processed and indexed successfully",
            "result": result  # You can modify what you want to return from result
        }

    except Exception as e:
        print("❌ Error during embedding/indexing:", str(e))
        return {
            "status": "error",
            "message": f"Embedding failed: {str(e)}"
        }

@app.post("/run-process-documents")
async def run_process_documents():
    """Call the registered 'process_documents' MCP tool."""

    # Debug print to check available attributes and methods of mcp
    print(dir(mcp))  

    # Use list_tools() to find available tools or check via mcp.tool directly
    tools = await mcp.list_tools()  # Await the coroutine
    print("Available tools:", tools)

    # Check if 'process_documents' tool exists in the list of tools
    process_documents_tool = next((tool for tool in tools if tool.name == 'process_documents'), None)

    if process_documents_tool is None:
        raise HTTPException(status_code=404, detail="Tool 'process_documents' not found")

    try:
        # Create an empty argument dictionary or fetch required arguments as per the input schema
        arguments = {}  # This is empty based on the inputSchema, you can update this if needed

        # Call the tool function using mcp.call_tool with arguments
        result = await mcp.call_tool('process_documents', arguments)  # Pass the arguments as needed
        return {"status": "success", "message": "process_documents executed", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error executing tool: {e}")

@app.get("/")
def root():
    return {"message": "MCP FastAPI is running"}
