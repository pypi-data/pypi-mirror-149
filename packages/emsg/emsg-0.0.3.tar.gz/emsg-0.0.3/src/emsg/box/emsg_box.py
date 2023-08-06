import string
from emsg.box import full_box
from emsg.box import id3v2


class Builder:

    scheme_id_uri: string = "https://aomedia.org/emsg/ID3"
    value: string = "1"
    timescale: int = 0
    presentation_time_delta: int = 0
    presentation_time: int = 0
    event_duration: int = 0
    id: int = 0
    message_data: string = ""

    _full_box_builder: full_box.Builder
    _boxtype: string = "emsg"
    _uses_id3_over_emsg: bool = False

    def __init__(
        self, value: string, id: int, message_data: string, version: int = 1
    ) -> None:
        self._full_box_builder = full_box.Builder(
            boxtype=self._boxtype, version=version
        )
        # super().__init__(boxtype=self._boxtype, version=version)
        self.value = value
        self.id = id
        self.message_data = message_data
        self.version = version

    def build(self) -> bytes:
        scheme_id_uri = (self.scheme_id_uri + "\0").encode("utf-8")
        value = (self.value + "\0").encode("utf-8")
        timescale = bytes.fromhex(hex(self.timescale)[2:].rjust(int(32 / 4), "0"))

        event_duration = bytes.fromhex(
            hex(self.event_duration)[2:].rjust(int(32 / 4), "0")
        )
        id = bytes.fromhex(hex(self.id)[2:].rjust(int(32 / 4), "0"))

        if self.version == 0:
            presentation_time_delta = bytes.fromhex(
                hex(self.presentation_time_delta)[2:].rjust(int(32 / 4), "0")
            )
            message_data = self.message_data.encode("utf-8")
            return self._full_box_builder.set_user_data(
                scheme_id_uri
                + value
                + timescale
                + presentation_time_delta
                + event_duration
                + id
                + message_data
            ).build()

        else:  # self.version == 1
            presentation_time = bytes.fromhex(
                hex(self.presentation_time)[2:].rjust(int(64 / 4), "0")
            )
            if self._uses_id3_over_emsg:
                message_data = id3v2.Builder(txxx_frame_info=self.message_data).build()
            else:
                message_data = self.message_data.encode("utf-8")
            return self._full_box_builder.set_user_data(
                timescale
                + presentation_time
                + event_duration
                + id
                + scheme_id_uri
                + value
                + message_data
            ).build()

    def set_scheme_id_uri(self, scheme_id_uri: string) -> "Builder":
        self.scheme_id_uri = scheme_id_uri
        return self

    def set_presentation_time_delta(self, presentation_time_delta: int) -> "Builder":
        self.presentation_time_delta = presentation_time_delta
        return self

    def set_presentation_time(self, presentation_time: int) -> "Builder":
        self.presentation_time = presentation_time
        return self

    def set_timescale(self, timescale: int) -> "Builder":
        self.timescale = timescale
        return self

    def set_event_duration(self, event_duration: int) -> "Builder":
        self.event_duration = event_duration
        return self

    def set_uses_id3_over_emsg(self, uses_id3_over_emsg: bool) -> "Builder":
        self._uses_id3_over_emsg = uses_id3_over_emsg
        return self
