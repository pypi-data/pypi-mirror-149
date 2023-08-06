import string


class Builder:
    size: int
    type: int

    _boxtype: string
    _user_data: bytes

    def __init__(self, boxtype: string) -> None:
        self._boxtype = boxtype

    def build(self) -> bytes:
        id = self._boxtype.encode("utf-8")
        payload = id + self._user_data
        size_payload = len(payload) + 4
        size = bytes.fromhex(hex(size_payload)[2:].rjust(int(32 / 4), "0"))

        return size + payload

    def set_user_data(self, user_data: bytes) -> "Builder":
        self._user_data = user_data
        return self
