# jobs.py (or another module name if you prefer)
from mcp_server import mcp
import asyncio

async def run_process_documents_job():
    return await mcp.call_tool('process_documents', {})

async def run_process_html_job(arguments):
    return await mcp.call_tool('process_html', arguments)

def run_sync_process_documents_job():
    """Wrapper to run async job in sync environment"""
    return asyncio.run(run_process_documents_job())

def run_sync_process_html_job(arguments):
    """Wrapper to run async job in sync environment"""
    return asyncio.run(run_process_html_job(arguments))
