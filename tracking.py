#!/usr/bin/env python3
# USPS API Tracking
# Tested on Python 3.4.2 running on Debian 8.4
# https://github.com/LiterallyLarry/USPS-Tracking-Python
#
# You must provide your API key in Line 13 before running this program! You can sign up for an API key here: https://www.usps.com/business/web-tools-apis/welcome.htm

from urllib import request, parse
from sys import argv
from xml.etree import ElementTree

def usps_track(numbers_list):
    api_key = "YOUR_API_KEY_HERE";
    usps_url = "http://production.shippingapis.com/ShippingAPI.dll?API=TrackV2";
    xml = "<TrackRequest USERID=\"%s\">" % api_key;
    for track_id in numbers_list:
        xml += "<TrackID ID=\"%s\"></TrackID>" % track_id;
    xml += "</TrackRequest>";
    target = "%s&%s" % (usps_url, parse.urlencode({ "XML" : xml }));
    request_obj = request.urlopen(target);
    result = request_obj.read();
    request_obj.close();
    return result;

if __name__ == "__main__":
    if len(argv) > 1: # System arguments support multiple tracking numbers
        track_ids = argv[1:];
    else:
        track_id = input('Enter a tracking number: '); # User input prompt supports only a single number
        if len(track_id) < 1:
            exit(0);
        track_ids = [ track_id ];
    track_xml = usps_track(track_ids);
    track_result = ElementTree.ElementTree(ElementTree.fromstring(track_xml));
    for result in track_result.findall('Description'): # Print error messages
        print(result.text);
    for result in track_result.findall('.//TrackSummary'): # Print tracking messages
        print(result.text);
