"""Pydantic models for the CUA Cloud provider API.

Documents the response shape for the Cloud list VMs endpoint.

List VMs
- Method: GET
- Path: `/v1/vms`
- Description: Returns all VMs owned by the API key's user.
- Responses:
  - 200: Array of minimal VM objects with fields `{ name, password, status }`
  - 401: Unauthorized (missing/invalid API key)

Example curl:
    curl -H "Authorization: Bearer $CUA_API_KEY" \
         "https://api.cua.ai/v1/vms"

Response shape:
[
  {
    "name": "s-windows-x4snp46ebf",
    "password": "49b8daa3",
    "status": "running"
  }
]

Status values:
- pending   : VM deployment in progress
- running   : VM is active and accessible
- stopped   : VM is stopped but not terminated
- terminated: VM has been permanently destroyed
- failed    : VM deployment or operation failed
"""
from __future__ import annotations

from typing import Literal, Optional

# Require pydantic for typed models in provider APIs
from pydantic import BaseModel


CloudVMStatus = Literal["pending", "running", "stopped", "terminated", "failed"]


class CloudVM(BaseModel):
    """Minimal VM object returned by CUA Cloud list API.

    Additional optional fields (like URLs) may be filled by callers based on
    their environment but are not guaranteed by the API.
    """

    name: str
    password: str
    status: CloudVMStatus

    # Optional, not guaranteed by the list API, but useful when known/derived
    vnc_url: Optional[str] = None
    api_url: Optional[str] = None
