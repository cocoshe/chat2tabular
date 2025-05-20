import logging
import os
from typing import Any, List, Dict
import pandas

from mcp.server.fastmcp import FastMCP



ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LOG_FILE = os.path.join(ROOT_DIR, "tabular-mcp.log")

# Initialize TABULAR_FILES_PATH variable without assigning a value
TABULAR_FILES_PATH = None

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        # Referring to https://github.com/modelcontextprotocol/python-sdk/issues/409#issuecomment-2816831318
        # The stdio mode server MUST NOT write anything to its stdout that is not a valid MCP message.
        logging.FileHandler(LOG_FILE)
    ],
)
logger = logging.getLogger("chat2tabular")
# Initialize FastMCP server
mcp = FastMCP(
    "chat2tabular",
    env_vars={
        "TABULAR_FILES_PATH": {
            "description": "Path to tabular files directory",
            "required": False,
            "default": TABULAR_FILES_PATH
        }
    }
)



async def run_sse():
    """Run Tabular MCP server in SSE mode."""
    # Assign value to TABULAR_FILES_PATH in SSE mode
    global TABULAR_FILES_PATH
    TABULAR_FILES_PATH = os.environ.get("TABULAR_FILES_PATH", "./tabular_files")
    # Create directory if it doesn't exist
    os.makedirs(TABULAR_FILES_PATH, exist_ok=True)
    
    try:
        logger.info(f"Starting Tabular MCP server with SSE transport (files directory: {TABULAR_FILES_PATH})")
        await mcp.run_sse_async()
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
        await mcp.shutdown()
    except Exception as e:
        logger.error(f"Server failed: {e}")
        raise
    finally:
        logger.info("Server shutdown complete")

def run_stdio():
    """Run Tabular MCP server in stdio mode."""
    # No need to assign TABULAR_FILES_PATH in stdio mode
    
    try:
        logger.info("Starting Tabular MCP server with stdio transport")
        mcp.run(transport="stdio")
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server failed: {e}")
        raise
    finally:
        logger.info("Server shutdown complete")



@mcp.tool()
async def hello(query: str) -> str:
    return f"Hello, {query}!"

@mcp.tool()
async def create_tabular_file(
    file_path: str,
) -> Dict[str, Any]:
    """Create a new tabular file."""
    # Check if file already exists
    if os.path.exists(file_path):
        raise FileExistsError(f"File {file_path} already exists.")
    
    # Create a new DataFrame and save it to the specified file
    df = pandas.DataFrame()
    df.to_csv(file_path, index=False)
    
    return {"message": f"File {file_path} created successfully."}
    
    