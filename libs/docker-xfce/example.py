#!/usr/bin/env python3
"""
Example script demonstrating how to use the CUA Docker XFCE container
with the Computer library.
"""

import asyncio
from computer import Computer


async def basic_example():
    """Basic example: Take a screenshot and click around"""
    print("=== Basic Example ===")

    computer = Computer(
        os_type="linux",
        provider_type="docker",
        image="trycua/cua-docker-xfce:latest",
        display="1920x1080",
        memory="4GB",
        cpu="2",
        port=8000,
        noVNC_port=6901
    )

    async with computer:
        print("Computer is ready!")
        print(f"noVNC available at: http://localhost:6901")

        # Get screen info
        screen = await computer.interface.get_screen_size()
        print(f"Screen size: {screen['width']}x{screen['height']}")

        # Take a screenshot
        screenshot = await computer.interface.screenshot()
        with open("screenshot.png", "wb") as f:
            f.write(screenshot)
        print("Screenshot saved to screenshot.png")

        # Click and type
        await computer.interface.left_click(100, 100)
        await computer.interface.type_text("Hello from CUA!")

        print("Done!")


async def file_operations_example():
    """Example: File system operations"""
    print("\n=== File Operations Example ===")

    computer = Computer(
        os_type="linux",
        provider_type="docker",
        image="trycua/cua-docker-xfce:latest"
    )

    async with computer:
        # Create a file
        await computer.interface.write_text(
            "/home/cua/test.txt",
            "Hello from CUA!"
        )
        print("Created test.txt")

        # Read it back
        content = await computer.interface.read_text("/home/cua/test.txt")
        print(f"File content: {content}")

        # List directory
        files = await computer.interface.list_dir("/home/cua")
        print(f"Files in home directory: {files}")


async def command_execution_example():
    """Example: Running shell commands"""
    print("\n=== Command Execution Example ===")

    computer = Computer(
        os_type="linux",
        provider_type="docker",
        image="trycua/cua-docker-xfce:latest"
    )

    async with computer:
        # Run a command
        result = await computer.interface.run_command("uname -a")
        print(f"System info:\n{result.stdout}")

        # Check Firefox is installed
        result = await computer.interface.run_command("which firefox")
        print(f"Firefox location: {result.stdout.strip()}")

        # Get Python version
        result = await computer.interface.run_command("python3 --version")
        print(f"Python version: {result.stdout.strip()}")


async def browser_automation_example():
    """Example: Opening Firefox and navigating"""
    print("\n=== Browser Automation Example ===")

    computer = Computer(
        os_type="linux",
        provider_type="docker",
        image="trycua/cua-docker-xfce:latest"
    )

    async with computer:
        # Open Firefox
        await computer.interface.run_command("firefox https://example.com &")
        print("Firefox opened")

        # Wait for it to load
        await asyncio.sleep(5)

        # Take a screenshot
        screenshot = await computer.interface.screenshot()
        with open("browser_screenshot.png", "wb") as f:
            f.write(screenshot)
        print("Browser screenshot saved")


async def persistent_storage_example():
    """Example: Using persistent storage"""
    print("\n=== Persistent Storage Example ===")

    computer = Computer(
        os_type="linux",
        provider_type="docker",
        image="trycua/cua-docker-xfce:latest",
        shared_directories=["./storage"]
    )

    async with computer:
        # Write to persistent storage
        await computer.interface.write_text(
            "/home/cua/storage/persistent.txt",
            "This file persists across container restarts!"
        )
        print("Written to persistent storage")

        # Read it back
        content = await computer.interface.read_text(
            "/home/cua/storage/persistent.txt"
        )
        print(f"Content: {content}")


async def multi_action_example():
    """Example: Complex interaction sequence"""
    print("\n=== Multi-Action Example ===")

    computer = Computer(
        os_type="linux",
        provider_type="docker",
        image="trycua/cua-docker-xfce:latest"
    )

    async with computer:
        # Open terminal
        await computer.interface.hotkey("ctrl", "alt", "t")
        await asyncio.sleep(2)

        # Type a command
        await computer.interface.type_text("echo 'Hello from CUA!'")
        await computer.interface.press_key("Return")
        await asyncio.sleep(1)

        # Take screenshot
        screenshot = await computer.interface.screenshot()
        with open("terminal_screenshot.png", "wb") as f:
            f.write(screenshot)
        print("Terminal screenshot saved")


async def main():
    """Run all examples"""
    examples = [
        ("Basic", basic_example),
        ("File Operations", file_operations_example),
        ("Command Execution", command_execution_example),
        ("Browser Automation", browser_automation_example),
        ("Persistent Storage", persistent_storage_example),
        ("Multi-Action", multi_action_example),
    ]

    print("Available examples:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"{i}. {name}")
    print(f"{len(examples) + 1}. Run all")

    choice = input("\nSelect an example (1-7): ").strip()

    try:
        if choice == str(len(examples) + 1):
            # Run all examples
            for name, func in examples:
                try:
                    await func()
                except Exception as e:
                    print(f"Error in {name}: {e}")
        else:
            idx = int(choice) - 1
            if 0 <= idx < len(examples):
                await examples[idx][1]()
            else:
                print("Invalid choice")
    except ValueError:
        print("Invalid input")


if __name__ == "__main__":
    asyncio.run(main())
