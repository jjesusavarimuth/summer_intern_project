import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from .manager import Manager


async def main() -> None:
    await Manager().run()


if __name__ == "__main__":
    asyncio.run(main())
