import string

class Builder:
    __txxx_frame_info: string

    def __init__(self, txxx_frame_info: string) -> None:
        self.__txxx_frame_info = txxx_frame_info

    def build(self) -> bytes:
        txxx_frame = self.__txxx_frame()
        id3v2_header = self.__id3v2_header(len(txxx_frame))
        return id3v2_header + txxx_frame

    def __id3v2_header(self, size: int) -> bytes:
        id3v2_id = 'ID3'.encode('utf-8')
        id3v2_version = bytes([0x04, 0x00])
        id3v2_flag = self.__id3v2_flag()
        id3v2_size = self.__syncsafe_bytes(size)
        return id3v2_id + id3v2_version + id3v2_flag + id3v2_size

    def __id3v2_flag(self, unsynchronisation=False, extension_header=False, experimental_indicator=False, id3v2_footer=False) -> bytes:
        flag_bytes = bytes(8)
        if unsynchronisation:
            flag_bytes += 1 << 7
        if extension_header:
            flag_bytes += 1 << 6
        if experimental_indicator:
            flag_bytes += 1 << 5
        if id3v2_footer:
            flag_bytes += 1 << 4
        return flag_bytes

    def __txxx_frame(self) -> bytes:
        frame_field = self.__txxx_frame_field()
        frame_header = self.__txxx_frame_header(frame_field)
        return frame_header + frame_field

    def __txxx_frame_header(self, frame_field: bytes) -> bytes:
        frame_id = 'TXXX'.encode('utf-8')
        frame_size = self.__syncsafe_bytes(len(frame_field))
        frame_flag = self.__txxx_frame_flag()
        return frame_id + frame_size + frame_flag
    
    def __txxx_frame_field(self) -> bytes:
        text_encoding = (3).to_bytes(1, 'big')
        description = 'Description'.encode('utf-8')
        delimiter = bytes(1)
        value = self.__txxx_frame_info.encode('utf-8')
        return text_encoding + description + delimiter + value

    def __txxx_frame_flag(self, tag_alter_preservation=False, file_alter_preservation=False, read_only=False, grouping_identity=False, compression=False, encryption=False, unsynchronisation=False, data_length_indicator=False) -> bytes:
        frame_status_flags = bytes(1)
        flag = bytes(2)
        if tag_alter_preservation:
            frame_status_flags[0] = frame_status_flags[0] + (1 << 6)
        if file_alter_preservation:
            frame_status_flags[0] = frame_status_flags[0] + (1 << 5)
        if read_only:
            frame_status_flags[0] = frame_status_flags[0] + (1 << 4)
        
        frame_format_flags = bytes(1)
        if grouping_identity:
            frame_format_flags[0] = frame_format_flags[0] + (1 << 6)
        if compression:
            frame_format_flags[0] = frame_format_flags[0] + (1 << 3)
        if encryption:
            frame_format_flags[0] = frame_format_flags[0] + (1 << 2)
        if unsynchronisation:
            frame_format_flags[0] = frame_format_flags[0] + (1 << 1)
        if data_length_indicator:
            frame_format_flags[0] = frame_format_flags[0] + (1 << 0)
        
        return frame_status_flags + frame_format_flags

    def __syncsafe_bytes(self, number: int) -> bytes:
        bin_str = bin(number)[2:].rjust(int(4*7), '0')
        for i in range(3):
            bin_str = bin_str[:(i+1)*7] + '0' + bin_str[(i+1)*7:]

        syncsafe_int = int('0b' + bin_str, base=0)
        syncsafe_bytes = syncsafe_int.to_bytes(4, 'big')

        return syncsafe_bytes
