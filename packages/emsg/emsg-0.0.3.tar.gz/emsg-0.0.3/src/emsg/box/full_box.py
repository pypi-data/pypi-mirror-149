import string
from emsg import box


class Builder:
    version: int
    flags: int

    _box_builder: box.Builder
    _full_box_user_data: bytes

    def __init__(self, boxtype: string, version: int, flags=0) -> None:
        self._box_builder = box.Builder(boxtype=boxtype)
        self.version = version
        self.flags = flags

    def build(self) -> bytes:
        version = bytes.fromhex(hex(self.version)[2:].rjust(int(8 / 4), "0"))
        flags = bytes.fromhex(hex(self.version)[2:].rjust(int(24 / 4), "0"))
        return self._box_builder.set_user_data(
            version + flags + self._full_box_user_data
        ).build()

    def set_user_data(self, user_data: bytes) -> "Builder":
        self._full_box_user_data = user_data
        return self
