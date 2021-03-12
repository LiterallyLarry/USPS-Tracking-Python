# USPS-Tracking-Python
![PyPI - License](https://img.shields.io/pypi/l/usps-tracking-tool) ![PyPI](https://img.shields.io/pypi/v/usps-tracking-tool)

Command line utility to track your packages using the USPS Track Request API.

A simple CLI package tracking tool with no Python dependencies required.

IMPORTANT: You must provide your API key first before using.
Sign up at: https://www.usps.com/business/web-tools-apis/welcome.htm

You may provide the USPS API key in the config.json file or as an 
environment variable: `USPS_API_KEY`, please see the [Providing API key](#providing-api-key) 
section for more information.

## Installation

Available through PyPI: https://pypi.org/project/usps-tracking-tool/

`pip3 install usps-tracking-tool`

After installing, you can run this program by using the command `usps-tracking-tool`.

## Providing API key

This program checks for the USPS API key using the following order:

1. API key passed in via the -a parameter.
2. API key provided in the config.json file.
3. API key provided in the environment variable `USPS_API_KEY`.

If an API key is not found in any of these places, the program will output an error and exit.

## Providing API key as an environment variable

You can set the API key in your CLI by using the below commands (matching your OS/terminal):

Unix Shell (Linux/MacOS):

`export USPS_API_KEY=your_api_key_here`

Command Prompt (Windows):

`set USPS_API_KEY=your_api_key_here`

Windows PowerShell (Windows):

`$Env:USPS_API_KEY = "your_api_key_here"`

## Usage

If running from the project directory, the program is available in the `usps_tracking_tool` folder. 
In that case, please substitute the `usps-tracking-tool` command in the below examples with `python3 tracking.py`.

You can track single/multiple shipment(s) by executing the program as follows:

```
usps-tracking-tool
usps-tracking-tool ABC1234567890
usps-tracking-tool ABC1234567890 DEF1234567890 GHI1234567890
```

If you run the program without a tracking number, it will prompt you for a tracking number (you may input multiple tracking numbers by separating them with spaces).

## Examples

```
user@system:~$ usps-tracking-tool
Enter tracking numbers separated by spaces: ABC1234567890 DEF1234567890 GHI1234567890

Package #1:
 Your item arrived at the PHILADELPHIA, PA 19101 post office at 11:02 am on June 19, 2017 and is ready for pickup.
  ├ Arrived at Unit, June 19, 2017, 10:33 am, PHILADELPHIA, PA 19104
  ├ Departed USPS Facility, June 17, 2017, 2:40 pm, PHILADELPHIA, PA 19116
  ├ Arrived at USPS Facility, June 17, 2017, 2:22 pm, PHILADELPHIA, PA 19116
  ├ Processed Through Facility, June 15, 2017, 1:29 am, ISC NEW YORK NY(USPS)
  ├ Origin Post is Preparing Shipment
  ├ Processed Through Facility, June 10, 2017, 6:00 am, TOKYO INT V BAG 2, JAPAN
  └ Acceptance, June 6, 2017, 1:26 pm, JAPAN

Package #2:
 Your item was delivered at 6:14 pm on July 6, 2017 in PHILADELPHIA, PA 19104.
  ├ Sorting Complete, July 6, 2017, 10:29 am, PHILADELPHIA, PA 19101
  ├ Available for Pickup, July 6, 2017, 8:29 am, PHILADELPHIA, PA 19101
  ├ Arrived at Post Office, July 6, 2017, 8:05 am, PHILADELPHIA, PA 19104
  ├ Arrived at USPS Destination Facility, July 6, 2017, 2:00 am, PHILADELPHIA, PA 19176
  ├ Processed Through Facility, July 5, 2017, 6:41 pm, ISC NEW YORK NY(USPS)
  ├ Origin Post is Preparing Shipment
  ├ Processed Through Facility, July 5, 2017, 6:20 am, TOKYO INT CONTAINER 1, JAPAN
  ├ Processed Through Facility, July 4, 2017, 8:01 pm, TOKYO INT, JAPAN
  └ Acceptance, July 4, 2017, 4:00 pm, JAPAN

Package #3:
 The Postal Service could not locate the tracking information for your request. Please verify your tracking number and try again later.
```

##### You can use arguments to change the output format, like so:

```
user@system:~$ usps-tracking-tool -h
usage: usps-tracking-tool [-h] [-s] [-n] [-m] [-d] [-a USPS_API_KEY]
                   [TRACKING_NUMBER [TRACKING_NUMBER ...]]

Tracks USPS numbers via Python.

positional arguments:
  TRACKING_NUMBER  a tracking number

optional arguments:
  -h, --help       show this help message and exit
  -s               Show tracking number in output
  -n               Hide extended tracking information
  -m               Display tracking information concisely (minimal UI)
  -d               Display the API key currently being used
  -a USPS_API_KEY  Manually provide the USPS API key to the program
```

```
user@system:~$ usps-tracking-tool ABC1234567890 -m
Your item was delivered at 6:14 pm on July 6, 2017 in PHILADELPHIA, PA 19104.
  ├ Sorting Complete, July 6, 2017, 10:29 am, PHILADELPHIA, PA 19101
  ├ Available for Pickup, July 6, 2017, 8:29 am, PHILADELPHIA, PA 19101
  ├ Arrived at Post Office, July 6, 2017, 8:05 am, PHILADELPHIA, PA 19104
  ├ Arrived at USPS Destination Facility, July 6, 2017, 2:00 am, PHILADELPHIA, PA 19176
  ├ Processed Through Facility, July 5, 2017, 6:41 pm, ISC NEW YORK NY(USPS)
  ├ Origin Post is Preparing Shipment
  ├ Processed Through Facility, July 5, 2017, 6:20 am, TOKYO INT CONTAINER 1, JAPAN
  ├ Processed Through Facility, July 4, 2017, 8:01 pm, TOKYO INT, JAPAN
  └ Acceptance, July 4, 2017, 4:00 pm, JAPAN
```

```
user@system:~$ usps-tracking-tool ABC1234567890 -mn
Your item was delivered at 6:14 pm on July 6, 2017 in PHILADELPHIA, PA 19104.
```

##### Check where the API key is being sourced from

```
user@system:~$ usps-tracking-tool -d
The current API key being used is: API_KEY_HERE
API key is being sourced from environment variable USPS_API_KEY
```

##### Manually provided API key

```
user@system:~$ usps-tracking-tool -a MANUALLY_PROVIDED_API_KEY -d
The current API key being used is: MANUALLY_PROVIDED_API_KEY
API key is being manually provided by -a parameter
```

This program was tested with Python 3.5.3 on Debian 10, Python 3.6.8 on Ubuntu 18.04, and may not be compatible with previous releases.

