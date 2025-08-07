"""
Required environment variables:
- CUA_API_KEY: API key for Cua cloud provider
"""

import os
import pytest
from pathlib import Path
import sys

# Load environment variables from .env file
project_root = Path(__file__).parent.parent
env_file = project_root / ".env"
print(f"Loading environment from: {env_file}")
from dotenv import load_dotenv

load_dotenv(env_file)

# Add paths to sys.path if needed
pythonpath = os.environ.get("PYTHONPATH", "")
for path in pythonpath.split(":"):
    if path and path not in sys.path:
        sys.path.insert(0, path)  # Insert at beginning to prioritize
        print(f"Added to sys.path: {path}")

from core.telemetry import record_event

@pytest.mark.asyncio(loop_scope="session")
async def test_telemetry():
    record_event("test_telemetry", {"message": "Hello, world!"})

if __name__ == "__main__":
    # Run tests directly
    pytest.main([__file__, "-v"])
