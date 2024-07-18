import json
import os
import sys
import re
from datetime import datetime


def lint():
    file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "certs.json")
    if not os.path.isfile(file_path):
        print("Can't find the file, quitting")
        sys.exit(1)

    with open(file_path) as f:
        data = json.load(f)

    existing_certs = []
    params = ["organization", "not_before", "not_after", "subject", "issuer"]

    for entry in data["certificates"]:
        if "sha1" not in entry.keys():
            print("Missing sha1 for entry {}".format(entry))
            continue
        if len(entry["sha1"]) != 40:
            print("Invalid SHA1 hash for {}".format(entry))

        for param in params:
            if param not in entry.keys():
                print("Missing param {} for cert {}".format(param, entry["sha1"]))

        if entry["sha1"].upper() != entry["sha1"]:
            print("Entry {} not in upper case".format(entry["sha1"]))

        if entry["sha1"].upper() in existing_certs:
            print("Duplicated entry {}".format(entry["sha1"].upper()))
        else:
            existing_certs.append(entry["sha1"].upper())

        # Check date format
        if "not_before" in entry.keys():
            if (
                re.fullmatch("\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}", entry["not_before"])
                is None
            ):
                print(
                    "Invalid not_before date format for entry {} : {}".format(
                        entry["sha1"], entry["not_before"]
                    )
                )
        if "not_after" in entry.keys():
            if (
                re.fullmatch("\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}", entry["not_after"])
                is None
            ):
                print(
                    "Invalid not_after date format for entry {} : {}".format(
                        entry["sha1"], entry["not_after"]
                    )
                )
        # if "not_after" in entry.keys() and "not_before" in entry.keys():
        # not_before = datetime.strptime(entry["not_before"], "%Y-%m-%dT%H:%M:%S")
        # not_after = datetime.strptime(entry["not_after"], "%Y-%m-%dT%H:%M:%S")
        # if not_before > not_after:
        # print(
        # "Invalid before/after dates in certificate {}".format(entry["sha1"])
        # )
    print("{} certificates".format(len(existing_certs)))


if __name__ == "__main__":
    lint()
