import asyncio
import os
from typing import List, Dict, Any

from computer.providers.cloud.provider import CloudProvider

async def main() -> None:
    api_key = os.getenv("CUA_API_KEY")
    if not api_key:
        raise RuntimeError(
            "CUA_API_KEY environment variable is not set.\n"
            "Set it and re-run, e.g.:\n"
            "  PowerShell: $env:CUA_API_KEY='your-key'\n"
            "  bash:       export CUA_API_KEY=your-key"
        )
    # List VMs
    provider = CloudProvider(api_key=api_key, verbose=True)
    async with provider:
        vms = await provider.list_vms()
        if not vms:
            print("No VMs returned (check API key or account).")
        else:
            print(f"Found {len(vms)} VM(s):")
            for i, vm in enumerate(vms, start=1):
                # Typical fields: name, status (if available), region, os_type, etc. (depends on account)
                print(f"[{i}] {vm}")

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
