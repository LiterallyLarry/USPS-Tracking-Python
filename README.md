# USPS-Tracking-Python
Track your packages with the USPS Track Request API using Python 3

IMPORTANT! You must provide your API key (sign up at https://www.usps.com/business/web-tools-apis/welcome.htm) in Line 13 before use!

## Example

```
user@system:~$ python3 tracking.py ABC1234567890 DEF1234567890 GHI1234567890
Your item arrived at our HURON, SD 57399 origin facility on July 12, 2016 at 9:16 pm. The item is currently in transit to the destination.
Your item was accepted at 2:44 pm on July 14, 2016 in JAPAN.
Your item arrived at our CHICAGO METRO origin facility on July 13, 2016 at 9:17 pm. The item is currently in transit to the destination.
```

## Usage

You can track a single/multiple shipment as follows:

```
python3 tracking.py
python3 tracking.py ABC1234567890
python3 tracking.py ABC1234567890 DEF1234567890 GHI1234567890
```

If you run the program without a tracking number, it will prompt you for a single tracking number. You should use arguments for multiple package tracking.

This program was tested on Python 3.4.2 running on Debian 8.4 and may not be compatible with previous releases.