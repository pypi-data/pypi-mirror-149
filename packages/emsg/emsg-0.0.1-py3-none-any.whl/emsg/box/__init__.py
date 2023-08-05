import string

class Builder:
    size: int
    type: int

    def build(self, box_id: string, data: bytes) -> None:
        id = box_id.encode('utf-8')
        payload = id + data
        size_payload = len(payload) + 4
        size = bytes.fromhex(hex(size_payload)[2:].rjust(int(32 / 4), '0'))

        return size + payload
