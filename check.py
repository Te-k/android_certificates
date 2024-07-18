import json
import os
import sys
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Check if a certificate is in the list"
    )
    parser.add_argument("SHA1", help="Sha1 of the certificate")
    args = parser.parse_args()

    file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "certs.json")
    if not os.path.isfile(file_path):
        print("Can't find the file, quitting")
        sys.exit(1)

    with open(file_path) as f:
        data = json.load(f)

    for entry in data["certificates"]:
        if args.SHA1.upper() == entry["sha1"]:
            print("Found:")
            print(json.dumps(entry, indent=4))
            sys.exit(0)

    print("This certificate wasn't found in the list")
