#!/usr/bin/env python3
# USPS API Tracking
# Tested on Python 3.4.2 running on Debian 8.7
# https://github.com/LiterallyLarry/USPS-Tracking-Python
#
# You must provide your API key in config.json as "api_key" before running this program.
# You can sign up for an API key at https://www.usps.com/business/web-tools-apis/welcome.htm

from urllib import request, parse
from sys import argv
from xml.etree import ElementTree
import argparse, json, sys, os

USPS_API_URL = "https://production.shippingapis.com/ShippingAPI.dll?API=TrackV2"
API_KEY_CONFIG_FILE = "config.json"
API_KEY_ENV_VAR = "USPS_API_KEY"

def usps_track(api_key, numbers_list):
    xml = "<TrackRequest USERID=\"{}\">".format(api_key)
    for track_id in numbers_list:
        xml += "<TrackID ID=\"{}\"></TrackID>".format(track_id)
    xml += "</TrackRequest>"
    target = "{}&{}".format(USPS_API_URL, parse.urlencode({ "XML" : xml }))
    request_obj = request.urlopen(target)
    result = request_obj.read()
    request_obj.close()
    return result

def main():
    path = os.path.dirname(os.path.realpath(__file__))
    config_file_path = os.path.join(path, API_KEY_CONFIG_FILE)
    api_key_from_env = False
    api_key = None

    if os.path.isfile(config_file_path):
        with open(config_file_path) as config_file:
            config = json.load(config_file)
            api_key = config.get("api_key")

    if not api_key:
        api_key = os.getenv(API_KEY_ENV_VAR)
        api_key_from_env = True

    parser = argparse.ArgumentParser(description="Tracks USPS numbers via Python.")

    parser.add_argument("tracking_numbers", metavar="TRACKING_NUMBER", type=str, nargs="*",
                        help="a tracking number")
    parser.add_argument("-s", action="store_true", default=False,
                        dest="show_tracking_number",
                        help="Show tracking number in output")
    parser.add_argument("-n", action="store_false", default=True,
                        dest="show_tracking_extended",
                        help="Hide extended tracking information")
    parser.add_argument("-m", action="store_true", default=False,
                        dest="show_minimal",
                        help="Display tracking information concisely (minimal UI)")
    parser.add_argument("-d", action="store_true", default=False,
                        dest="display_api_key",
                        help="Display the API key currently being used")
    parser.add_argument("-a", action="store", default=None,
                        dest="usps_api_key",
                        help="Manually provide the USPS API key to the program")
    
    args = parser.parse_args()

    if args.usps_api_key is not None:
        api_key = args.usps_api_key
    elif not api_key:
        print("Error: Could not find USPS API key!")
        print("Please provide one in the {} file, as environment variable {}, or pass it in manually using the -a parameter.".format(API_KEY_CONFIG_FILE, API_KEY_ENV_VAR))
        print("Location of {} is: {}".format(API_KEY_CONFIG_FILE, config_file_path))
        sys.exit(2)

    if args.display_api_key:
        print("The current API key being used is: {}".format(api_key))
        if args.usps_api_key is not None:
            print("API key is being manually provided by -a parameter")
        elif api_key_from_env:
            print("API key is being sourced from environment variable {}".format(API_KEY_ENV_VAR))
        else:
            print("API key is being sourced from configuration file: {}".format(config_file_path))
        sys.exit(0)
    elif args.tracking_numbers: # Arguments support multiple tracking numbers
        track_ids = args.tracking_numbers
    else:
        track_id = input("Enter tracking numbers separated by spaces: ") # User input supports multiple tracking numbers split with spaces
        if len(track_id) < 1:
            exit(0)
        track_ids = track_id.split(" ")

    real = []
    for id in track_ids:
        if id[0] != "#":
            real.append(id)

    track_ids = real
    track_xml = usps_track(api_key, track_ids)
    track_result = ElementTree.ElementTree(ElementTree.fromstring(track_xml))
    
    if track_result.getroot().tag == "Error":
        error_number = track_result.find("Number").text
        error_message = track_result.find("Description").text
        print("An error has occurred (Error Number {}):\n{}".format(error_number, error_message))
        sys.exit(2)
    
    for result in track_result.findall("Description"):
        print(result.text)
    
    for number, result in enumerate(track_result.findall(".//TrackInfo")):
        if args.show_tracking_number:
            track_num = " ({})".format(track_ids[number])
        else:
            track_num = ""
        summary = result.find("TrackSummary")
        if summary is None:
            print("There was an error handling the XML response:\n{}".format(track_xml))
            sys.exit(2)
        else:
            if args.show_minimal:
                print(summary.text)
            else:
                print("\nPackage #{}{}:\n {}".format(number + 1, track_num, summary.text))
            if args.show_tracking_extended:
                details = result.findall("TrackDetail")
                for detail_number, detailed_result in enumerate(details):
                    if detail_number + 1 == len(details):
                        print("  └ {}".format(detailed_result.text))
                    else:
                        print("  ├ {}".format(detailed_result.text))

if __name__ == "__main__":
    main()
    
