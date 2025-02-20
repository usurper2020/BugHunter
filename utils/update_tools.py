"""
Tool update script for the BugHunter application.

This script provides automated updating of all installed security tools,
ensuring they are kept current with their respective repositories.
It handles the update process asynchronously for better performance.
"""

#!/usr/bin/env python3

import asyncio
import logging
from pathlib import Path
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tool_manager import ToolManager

async def update_all_tools(tool_manager: ToolManager):
    """
    Update all installed security tools asynchronously.
    
    Parameters:
        tool_manager (ToolManager): Instance of tool manager to use
                                  for updates
    
    This function:
    1. Checks status of each installed tool
    2. Updates tools that are confirmed as installed
    3. Processes updates concurrently using asyncio
    
    Note:
        Tools that fail status check are skipped for safety
    """
    for tool_name in tool_manager.tools:
        status = await tool_manager.check_tool_status(tool_name)
        if status.get('installed'):
            await tool_manager.update_tool(tool_name)

async def main():
    """
    Main entry point for the tool update process.
    
    This function:
    1. Sets up logging configuration
    2. Initializes the tool manager
    3. Executes the update process
    4. Handles any errors during update
    
    Returns:
        int: Exit code (0 for success, 1 for failure)
        
    Note:
        Uses asyncio for concurrent processing
        Logs all steps and any errors encountered
    """
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger('ToolUpdater')

    try:
        # Initialize tool manager
        tool_manager = ToolManager()

        # Update all tools
        logger.info("Starting tool updates...")
        await update_all_tools(tool_manager)
        logger.info("All tools updated successfully!")

    except Exception as e:
        logger.error(f"Update failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    asyncio.run(main())
