#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import csv
import re
import sys


def main():
    url = "https://www.macfound.org/grants/?page="
    page = 1
    first = True
    with open("data.csv", "w", newline="") as f:
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
            grants = soup.find("ul", {"class": "grant-list"})
            for grant in grants.find_all("li"):
                d = {}
                d['grantee'] = grant.find("h2").text
                d['url'] = (grant.find("h2").find("a") or {}).get("href")
                d['amount'] = grant.find("div", {"class": "amount"}).text
                d['date'] = grant.find("p", {"class": "activedate"}).find("strong").text
                temp = grant.find("p", {"class": "activedate"}).text.strip()
                m = re.search(r'\(Duration (.*)\)', temp)
                d['duration'] = m.group(1)
                d['location'] = grant.find("span").text.strip()

                cause_area = grant.find("p", {"class": "assignments"})
                if cause_area:
                    m = re.search(r'Learn more about (.*)$',
                                  cause_area.text.strip())
                    if m:
                        d['cause_area'] = m.group(1)
                    d['cause_area_url'] = cause_area.find("a").get("href")

                grant.find_all("p")[1].span.extract()  # remove the span tag
                notes = grant.find_all("p")[1].text.strip()
                assert notes.startswith("\u2013 ")
                d['notes'] = notes[len("\u2013 "):]
                writer.writerow(d)

            page += 1


if __name__ == "__main__":
    main()
