import string
from . import Builder as BoxBuilder

class Builder(BoxBuilder) :
    version: int
    flags: int = 0

    def __init__(self, version: int) -> None:
        super().__init__()
        self.version = version

    def build(self, box_id: string, data: bytes) -> None:
        version = bytes.fromhex(hex(self.version)[2:].rjust(int(8 / 4), '0'))
        flags = bytes.fromhex(hex(self.version)[2:].rjust(int(24 / 4), '0'))
        return super().build(box_id=box_id, data=(version + flags + data))
