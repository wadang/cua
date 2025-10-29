from typing import Optional

from .generic import GenericComputerInterface


class WindowsComputerInterface(GenericComputerInterface):
    """Interface for Windows."""

    def __init__(
        self,
        ip_address: str,
        username: str = "lume",
        password: str = "lume",
        api_key: Optional[str] = None,
        vm_name: Optional[str] = None,
        port: Optional[int] = None,
        secure_port: Optional[int] = None,
    ):
        super().__init__(
            ip_address,
            username,
            password,
            api_key,
            vm_name,
            port=port,
            secure_port=secure_port,
            logger_name="computer.interface.windows",
        )
