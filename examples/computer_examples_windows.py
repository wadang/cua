import os
import asyncio
from pathlib import Path
import sys
import traceback

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

from computer.computer import Computer
from computer.providers.base import VMProviderType
from computer.logger import LogLevel

async def main():
    try:
        print("\n=== Using direct initialization ===")

        # Create a remote Windows computer with Cua
        computer = Computer(
            os_type="windows",
            api_key=os.getenv("CUA_API_KEY"),
            name=os.getenv("CONTAINER_NAME") or "",
            provider_type=VMProviderType.CLOUD,
        )
        
        try:
            # Run the computer with default parameters
            await computer.run()
            
            screenshot = await computer.interface.screenshot()
            
            # Create output directory if it doesn't exist
            output_dir = Path("./output")
            output_dir.mkdir(exist_ok=True)
            
            # Mouse Actions Examples
            print("\n=== Mouse Actions ===")
            await computer.interface.move_cursor(100, 100)
            await computer.interface.left_click()
            await computer.interface.double_click(400, 400)
            await computer.interface.right_click(300, 300)

            # Command Actions Examples
            print("\n=== Command Actions ===")
            await computer.interface.run_command("notepad")

            screenshot_path = output_dir / "screenshot.png"
            with open(screenshot_path, "wb") as f:
                f.write(screenshot)
            print(f"Screenshot saved to: {screenshot_path.absolute()}")
            
            # Keyboard Actions Examples
            print("\n=== Keyboard Actions ===")
            await computer.interface.type_text("Hello, World!")
            await computer.interface.press_key("enter")

            # Clipboard Actions Examples
            print("\n=== Clipboard Actions ===")
            await computer.interface.set_clipboard("Test clipboard")
            content = await computer.interface.copy_to_clipboard()
            print(f"Clipboard content: {content}")

        finally:
            # Important to clean up resources
            await computer.stop()
    except Exception as e:
        print(f"Error in main: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
