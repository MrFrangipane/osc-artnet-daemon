from dataclasses import dataclass


@dataclass
class OSCClientInfo:
    address: bytes  # FIXME use ipaddress module
    id: bytes
    name: str
    port: int

    def __repr__(self):
        address_pretty = '.'.join(str(int(b)) for b in self.address)
        return (
            f"<OSCClient("
            f"address=[{address_pretty}], "
            f"id={self.id}, "
            f"name='{self.name}', "
            f"port={self.port}"
            f")>"
        )
