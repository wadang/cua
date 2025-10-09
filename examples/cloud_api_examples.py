import asyncio
import os
from utils import load_dotenv_files

load_dotenv_files()

from computer.providers.cloud.provider import CloudProvider

async def main() -> None:
    api_key = os.getenv("CUA_API_KEY")
    if not api_key:
        raise RuntimeError("CUA_API_KEY environment variable is not set")
    api_base = os.getenv("CUA_API_BASE")
    if api_base:
        print(f"Using API base: {api_base}")
    
    # List VMs
    provider = CloudProvider(api_key=api_key, verbose=True)
    async with provider:
        vms = await provider.list_vms()
        print(f"Found {len(vms)} VM(s)")
        for vm in vms:
            print(
                f"name: {vm['name']}\n",
                f"status: {vm['status']}\n", # pending, running, stopped, terminated, failed
                f"api_url: {vm.get('api_url')}\n",
                f"vnc_url: {vm.get('vnc_url')}\n",
            )

    # --- Additional operations (commented out) ---
    # To stop a VM by name:
    # api_key = os.getenv("CUA_API_KEY")
    # provider = CloudProvider(api_key=api_key, verbose=True)
    # async with provider:
    #     name = "your-vm-name-here"
    #     resp = await provider.stop_vm(name)
    #     print("stop_vm response:", resp)

    # To restart a VM by name:
    # api_key = os.getenv("CUA_API_KEY")
    # provider = CloudProvider(api_key=api_key, verbose=True)
    # async with provider:
    #     name = "your-vm-name-here"
    #     resp = await provider.restart_vm(name)
    #     print("restart_vm response:", resp)

    # To probe a VM's status via its public hostname (if you know the name):
    # api_key = os.getenv("CUA_API_KEY")
    # provider = CloudProvider(api_key=api_key, verbose=True)
    # async with provider:
    #     name = "your-vm-name-here"
    #     info = await provider.get_vm(name)
    #     print("get_vm info:", info)


if __name__ == "__main__":
    asyncio.run(main())
