#!/usr/bin/env python3
# License: CC0 https://creativecommons.org/publicdomain/zero/1.0/

import requests
from bs4 import BeautifulSoup
import csv
import re
import sys

import pdb


def main():
    url = "https://www.macfound.org/grants/?page="
    page = 1
    first = True
    with open(sys.argv[1], "w", newline="") as f:
        fieldnames = ["grantee", "url", "amount", "date", "duration",
                      "location", "notes", "cause_area", "cause_area_url"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        while True:
            print("Doing page", page, file=sys.stderr)
            r = requests.get(url + str(page))

            # We have reached the last page, so stop
            if r.status_code != 200:
                break

            soup = BeautifulSoup(r.content, "lxml")
            grants = [link for link in soup.find_all("a")
                      if link.get("href") and link.get("href").startswith("/grantees/")]
            for grant in grants:
                d = parse_grant(grant)
                writer.writerow(d)

            page += 1


def parse_grant(grant):
    """Take a grant HTML tag and convert it into a dictionary."""

    # Sanity check
    assert len(grant.find_all("div")) == 4

    d = {}
    d['grantee'] = grant.find("div").text.strip()
    d['url'] = grant.get("href")
    d['amount'] = grant.find("strong").contents[0]
    date_and_duration = grant.find("strong").contents[-1].split("•")
    assert len(date_and_duration) == 2, date_and_duration
    d['date'] = date_and_duration[0].strip()
    d['duration'] = date_and_duration[1].strip()
    location = grant.find_all("div")[2].text.strip().split("\n")[0]
    assert location.endswith(" -"), location
    d['location'] = location[:-len(" -")]
    d['cause_area'] = grant.find_all("div")[3].text.strip()
    d['notes'] = " ".join(grant.find_all("div")[2].text.strip().split("\n")[1:]).strip()

    return d


if __name__ == "__main__":
    main()
