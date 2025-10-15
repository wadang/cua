"""Launch two Docker-backed Computer instances simultaneously and perform basic actions.

This example spins up two independent Linux VMs using the Docker provider. Each VM
receives its own container name, API port, and VNC port so they can run in parallel
without fighting over shared resources. After performing a handful of interface
actions, the script captures a screenshot from each VM and stops both containers.

Prerequisites:
    * Docker is installed and running locally.
    * The requested image (default: trycua/cua-ubuntu:latest) is available, or
      Docker can pull it from a registry.
    * Optional: populate .env with override values for any COMPUTE_* variables
      referenced below.
"""

import asyncio
import logging
import os
import sys
import traceback
from pathlib import Path

from dotenv import load_dotenv

# Make sure environment variables from the project root are available.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = PROJECT_ROOT / ".env"
if ENV_FILE.exists():
    print(f"Loading environment from: {ENV_FILE}")
    load_dotenv(ENV_FILE)

# Respect any PYTHONPATH settings declared in the environment.
pythonpath = os.environ.get("PYTHONPATH", "")
for entry in pythonpath.split(":"):
    if entry and entry not in sys.path:
        sys.path.insert(0, entry)
        print(f"Added to sys.path: {entry}")

from computer.computer import Computer  # noqa: E402
from computer.providers.base import VMProviderType  # noqa: E402


DEFAULT_IMAGE = os.environ.get("COMPUTER_IMAGE", "trycua/cua-ubuntu:latest")
CONTAINER_PREFIX = os.environ.get("COMPUTER_CONTAINER_NAME", "cua-dual-example")
CONTAINER_ONE = os.environ.get("COMPUTER_CONTAINER_NAME_ONE", f"{CONTAINER_PREFIX}-one")
CONTAINER_TWO = os.environ.get("COMPUTER_CONTAINER_NAME_TWO", f"{CONTAINER_PREFIX}-two")

API_PORT_ONE = int(os.environ.get("COMPUTER_API_PORT_ONE", "18000"))
API_PORT_TWO = int(os.environ.get("COMPUTER_API_PORT_TWO", "18001"))
VNC_PORT_ONE = int(os.environ.get("COMPUTER_VNC_PORT_ONE", "16901"))
VNC_PORT_TWO = int(os.environ.get("COMPUTER_VNC_PORT_TWO", "16902"))

INTERFACE_DELAY = float(os.environ.get("COMPUTER_INTERFACE_DELAY", "0.1"))
OUTPUT_DIR = Path(os.environ.get("COMPUTER_OUTPUT_DIR", "./output"))


def resolve_verbosity(env_value: str | None) -> int:
    """Translate an environment string into a logging level integer."""
    if not env_value:
        return logging.INFO

    text = env_value.strip().lower()
    mapping = {
        "quiet": logging.WARNING,
        "warn": logging.WARNING,
        "warning": logging.WARNING,
        "normal": logging.INFO,
        "info": logging.INFO,
        "verbose": logging.DEBUG,
        "debug": logging.DEBUG,
    }
    if text in mapping:
        return mapping[text]

    try:
        return int(text)
    except ValueError:
        return logging.INFO


async def exercise_computer(
    *,
    name: str,
    api_port: int,
    vnc_port: int,
    text: str,
    command: str,
) -> None:
    """Spin up a Computer, run a few actions, capture a screenshot, then stop it."""
    computer = Computer(
        os_type="linux",
        provider_type=VMProviderType.DOCKER,
        image=DEFAULT_IMAGE,
        name=name,
        port=api_port,
        noVNC_port=vnc_port,
        verbosity=resolve_verbosity(os.environ.get("COMPUTER_LOG_LEVEL")),
    )

    await computer.run()
    try:
        computer.interface.delay = INTERFACE_DELAY

        print(f"[{name}] typing text...")
        await computer.interface.type_text(text)
        await computer.interface.press_key("enter")

        print(f"[{name}] running command: {command!r}")
        result = await computer.interface.run_command(command)
        print(f"[{name}] command exit {result.returncode}, stdout: {result.stdout.strip()}")
        if result.stderr:
            print(f"[{name}] stderr: {result.stderr.strip()}")

        print(f"[{name}] capturing screenshot...")
        screenshot = await computer.interface.screenshot()
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        screenshot_path = OUTPUT_DIR / f"{name}.png"
        screenshot_path.write_bytes(screenshot)
        print(f"[{name}] screenshot saved to: {screenshot_path.resolve()}")
    finally:
        print(f"[{name}] stopping computer...")
        # await computer.stop()
        print(f"[{name}] stopped.")


async def main() -> None:
    """Launch both Computers and wait for them to finish their workflows."""
    try:
        await asyncio.gather(
            exercise_computer(
                name=CONTAINER_ONE,
                api_port=API_PORT_ONE,
                vnc_port=VNC_PORT_ONE,
                text="Hello from the first Docker computer!",
                command="echo first-computer",
            ),
            exercise_computer(
                name=CONTAINER_TWO,
                api_port=API_PORT_TWO,
                vnc_port=VNC_PORT_TWO,
                text="Second computer reporting in.",
                command="echo second-computer",
            ),
        )
    except Exception as exc:
        print(f"Error while running dual computer example: {exc}")
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
