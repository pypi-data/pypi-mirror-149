# emsg

An ISO BMFF emsg atom generator.  This cli generates an emsg atom file with any given parameters.  You can insert it into an mp4 file by using an mp4 file editor such as Bento4's [mp4edit](https://www.bento4.com/documentation/mp4edit/) to deliver in-band media timed event data for MPEG-DASH, HLS, and so on.

## Usage

```sh
$ emsg --help
usage: emsg [-h] [-o OUT] [-s SCHEME_ID_URI] [--box_version {0,1}] [-i ID] [--value VALUE] [-m MESSAGE_DATA]
            [--presentation_time PRESENTATION_TIME] [--presentation_time_delta PRESENTATION_TIME_DELTA]
            [--timescale TIMESCALE] [--event_duration EVENT_DURATION]

options:
  -h, --help            show this help message and exit
  -o OUT, --out OUT     set file name to output (default=./emsg.atom)
  -s SCHEME_ID_URI, --scheme_id_uri SCHEME_ID_URI
                        set scheme id uri to identify the message scheme (default=https://aomedia.org/emsg/ID3)
  --box_version {0,1}   set emsg box version (default=1)
  -i ID, --id ID        set id (default=0)
  --value VALUE         set value for event stream elements (default=1)
  -m MESSAGE_DATA, --message_data MESSAGE_DATA
                        set message data
  --presentation_time PRESENTATION_TIME
                        set presentation time for emsg version 1 (default=450000)
  --presentation_time_delta PRESENTATION_TIME_DELTA
                        set presentation time delta for emsg version 0 (default=450000)
  --timescale TIMESCALE
                        set timescale (default=90000)
  --event_duration EVENT_DURATION
                        set event duration (default=270000)
```

### Examples

To generate an emsg box file named "sample-emsg.atom" containing the metadata below:

- timescale = 90000
- presentation time = 270000
- event duration = 180000
- id = 0
- scheme id uri = "urn:mpeg:dash:event:2012"
- value = "1"
- message data = "A sample message data"

Run the command below:

```sh
$ emsg -o sample-emsg.atom --timescale 90000 --presentation_time 270000 --event_duration 180000 -i 0 -s urn:mpeg:dash:event:2012 --value 1 -m "A sample message data"
```

## Format support

| Format | Supports |
| --- | --- |
| emsg version 0 | Y |
| emsg version 1 | Y |
| ID3 Metadata in emsg (version 1) | Y |
