# scripts/update_tools.py
#!/usr/bin/env python3

import asyncio
import logging
from pathlib import Path
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.tool_manager import ToolManager

async def update_all_tools(tool_manager: ToolManager):
    """Update all installed tools"""
    for tool_name in tool_manager.tools:
        status = await tool_manager.check_tool_status(tool_name)
        if status.get('installed'):
            await tool_manager.update_tool(tool_name)

async def main():
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger('ToolUpdater')

    try:
        # Initialize tool manager
        tool_manager = ToolManager(None)

        # Update all tools
        logger.info("Starting tool updates...")
        await update_all_tools(tool_manager)
        logger.info("All tools updated successfully!")

    except Exception as e:
        logger.error(f"Update failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    asyncio.run(main())
