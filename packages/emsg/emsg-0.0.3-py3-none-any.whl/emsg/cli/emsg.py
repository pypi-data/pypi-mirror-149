import argparse
import string
import sys
from emsg.box import emsg_box

SCHEME_ID_URI_EMSG_ID3 = "https://aomedia.org/emsg/ID3"
DEFAULT_OUT = "./emsg.atom"
DEFAULT_BOX_VERSION = 1
DEFAULT_VALUE = "1"
DEFAULT_ID = 0
DEFAULT_TIMESCALE = 90000
DEFAULT_EVENT_DURATION = 270000
DEFAULT_PRESENTATION_TIME_DELTA = 450000
DEFAULT_PRESENTATION_TIME = 450000

parser = argparse.ArgumentParser()
parser.add_argument(
    "-o",
    "--out",
    default=DEFAULT_OUT,
    help="set file name to output (default={})".format(DEFAULT_OUT),
)
parser.add_argument(
    "-s",
    "--scheme_id_uri",
    default=SCHEME_ID_URI_EMSG_ID3,
    help="set scheme id uri to identify the message scheme (default={})".format(
        SCHEME_ID_URI_EMSG_ID3
    ),
)
parser.add_argument(
    "--box_version",
    default=DEFAULT_BOX_VERSION,
    choices=[0, 1],
    help="set emsg box version (default={})".format(DEFAULT_BOX_VERSION),
)
parser.add_argument(
    "-i", "--id", default=DEFAULT_ID, help="set id (default={})".format(DEFAULT_ID)
)
parser.add_argument(
    "--value",
    default=DEFAULT_VALUE,
    help="set value for event stream elements (default={})".format(DEFAULT_VALUE),
)
parser.add_argument("-m", "--message_data", default="", help="set message data")
parser.add_argument(
    "--presentation_time",
    default=DEFAULT_PRESENTATION_TIME,
    help="set presentation time for emsg version 1 (default={})".format(
        DEFAULT_PRESENTATION_TIME
    ),
)
parser.add_argument(
    "--presentation_time_delta",
    default=DEFAULT_PRESENTATION_TIME_DELTA,
    help="set presentation time delta for emsg version 0 (default={})".format(
        DEFAULT_PRESENTATION_TIME_DELTA
    ),
)
parser.add_argument(
    "--timescale",
    default=DEFAULT_TIMESCALE,
    help="set timescale (default={})".format(DEFAULT_TIMESCALE),
)
parser.add_argument(
    "--event_duration",
    default=DEFAULT_EVENT_DURATION,
    help="set event duration (default={})".format(DEFAULT_EVENT_DURATION),
)

args = parser.parse_args()


def main():
    out = args.out
    version = int(args.box_version)
    value = args.value
    id = int(args.id)
    message_data = args.message_data
    scheme_id_uri = args.scheme_id_uri
    timescale = int(args.timescale)
    event_duration = int(args.event_duration)
    id3_over_emsg = scheme_id_uri == SCHEME_ID_URI_EMSG_ID3

    emsg_builder = (
        emsg_box.Builder(value=value, id=id, message_data=message_data, version=version)
        .set_scheme_id_uri(scheme_id_uri)
        .set_timescale(timescale)
        .set_event_duration(event_duration)
    )

    if version == 0 and hasattr(args, "presentation_time_delta"):
        emsg_builder.set_presentation_time_delta(
            int(args.presentation_time_delta or DEFAULT_PRESENTATION_TIME_DELTA)
        )
    elif version == 1 and hasattr(args, "presentation_time"):
        emsg_builder.set_presentation_time(
            int(args.presentation_time or DEFAULT_PRESENTATION_TIME)
        )

    emsg_builder.set_uses_id3_over_emsg(id3_over_emsg)

    atom = emsg_builder.build()
    writeToFile(atom, out)


def writeToFile(data: bytes, file_name: string):
    with open(file_name, "bw") as f:
        f.write(data)


if __name__ == "__main__":
    sys.exit(main())
