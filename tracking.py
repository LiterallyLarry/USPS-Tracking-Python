#!/usr/bin/env python3
# USPS API Tracking
# Tested on Python 3.4.2 running on Debian 8.7
# https://github.com/LiterallyLarry/USPS-Tracking-Python
#
# You must provide your API key in config.json as  before running this program! You can sign up for an API key here: https://www.usps.com/business/web-tools-apis/welcome.htm

from urllib import request, parse
from sys import argv
from xml.etree import ElementTree
import argparse, json, sys, os

USPS_API_URL = "http://production.shippingapis.com/ShippingAPI.dll?API=TrackV2";

path = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(path, "config.json")) as config_file:
    config = json.load(config_file);
    api_key = config.get("api_key");

if not api_key:
    sys.exit("Error: Could not find USPS API key in config.json!");

parser = argparse.ArgumentParser(description='Tracks USPS numbers via Python.');

parser.add_argument('tracking_numbers', metavar='TRACKING_NUMBER', type=str, nargs='*',
                    help='a tracking number');
parser.add_argument('-s', action='store_true', default=False,
                    dest='show_tracking_number',
                    help='Show tracking number in output');
parser.add_argument('-n', action='store_false', default=True,
                    dest='show_tracking_extended',
                    help='Hide extended tracking information');
parser.add_argument('-m', action='store_true', default=False,
                    dest='show_minimal',
                    help='Repress UI');

def usps_track(numbers_list):
    xml = "<TrackRequest USERID=\"%s\">" % api_key;
    for track_id in numbers_list:
        xml += "<TrackID ID=\"%s\"></TrackID>" % track_id;
    xml += "</TrackRequest>";
    target = "%s&%s" % (USPS_API_URL, parse.urlencode({ "XML" : xml }));
    request_obj = request.urlopen(target);
    result = request_obj.read();
    request_obj.close();
    return result;

if __name__ == "__main__":
    args = parser.parse_args();
    if args.tracking_numbers: # Arguments support multiple tracking numbers
        track_ids = args.tracking_numbers;
        #track_ids = argv[1:];
    else:
        #track_id = input(); # User input supports only a single number
        track_id = input('Enter tracking numbers separated by spaces: '); # User input supports multiple tracking numbers split with spaces
        if len(track_id) < 1:
            exit(0);
        track_ids = track_id.split(' ');
        #track_ids = [ track_id ];
    real = []
    for id in track_ids:
        if id[0] != '#':
            real.append(id);
    track_ids = real
    track_xml = usps_track(track_ids);
#    print(track_xml);
    track_result = ElementTree.ElementTree(ElementTree.fromstring(track_xml));
    if not args.show_minimal:
        print('OK!');
    for result in track_result.findall('Description'):
        print(result.text);
#    for result in track_result.findall('.//TrackSummary'):
#        print(result.text);
    for number, result in enumerate(track_result.findall('.//TrackInfo')):
        if args.show_tracking_number:
            track_num = ' (%s)' % track_ids[number];
        else:
            track_num = ''
        summary = result.find('TrackSummary');
        if summary is None:
            print('Error in XML!');
            print(track_xml);
        else:
            if args.show_minimal:
                print('%s' % summary.text);
            else:
                print('\nPackage #%d%s:\n %s' % (number+1,track_num,summary.text));
            if args.show_tracking_extended:
                details = result.findall('TrackDetail');
                for number_2, detailed_result in enumerate(details):
                    if number_2+1 == len(details):
                        print('  └ %s' % detailed_result.text);
                    else:
                        print('  ├ %s' % detailed_result.text);
