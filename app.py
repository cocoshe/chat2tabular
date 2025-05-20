import asyncio
import typer

from services.server import run_sse, run_stdio
from services.server import mcp

app = typer.Typer(help="MCP Server")


@app.command()
def sse():
    """Start MCP Server in SSE mode"""
    print("MCP Server - SSE mode")
    print("----------------------")
    print("Press Ctrl+C to exit")
    try:
        asyncio.run(run_sse())
    except KeyboardInterrupt:
        print("\nShutting down server...")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("Service stopped.")

@app.command()
def stdio():
    """Start MCP Server in stdio mode"""
    print("MCP Server - stdio mode")
    print("----------------------")
    print("Press Ctrl+C to exit")
    try:
        run_stdio()
    except KeyboardInterrupt:
        print("\nShutting down server...")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("Service stopped.")

if __name__ == "__main__":
    app() 