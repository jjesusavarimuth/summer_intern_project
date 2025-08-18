"""
Main Entry Point - CLI interface for the data analysis system.

This module provides the command-line interface for running the multi-agent
data analysis and visualization system outside of the Streamlit UI.
"""

import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from .manager import Manager

async def main() -> None:
    """Main entry point for CLI execution."""
    await Manager().run()

if __name__ == "__main__":
    asyncio.run(main())
