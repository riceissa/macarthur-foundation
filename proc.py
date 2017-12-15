#!/usr/bin/env python3
# License: CC0 https://creativecommons.org/publicdomain/zero/1.0/

import csv
import re


def mysql_quote(x):
    '''
    Quote the string x using MySQL quoting rules. If x is the empty string,
    return "NULL". Probably not safe against maliciously formed strings, but
    whatever; our input is fixed and from a basically trustable source..
    '''
    if not x:
        return "NULL"
    x = x.replace("\\", "\\\\")
    x = x.replace("'", "''")
    x = x.replace("\n", "\\n")
    return "'{}'".format(x)

def main():
    with open("data.csv", "r") as f:
        reader = csv.DictReader(f)
        first = True

        print("""insert into donations (donor, donee, amount, donation_date,
        donation_date_precision, donation_date_basis, cause_area, url,
        donor_cause_area_url, notes, affected_countries,
        affected_regions) values""")

        for row in reader:
            amount = row['amount']
            assert amount.startswith("$")
            amount = amount.replace("$", "").replace(",", "")
            donation_date = row['date']
            assert (len(donation_date) == 4 and
                    re.match(r'^\d\d\d\d$', donation_date) is not None)
            donation_date += "-01-01"

            print(("    " if first else "    ,") + "(" + ",".join([
                mysql_quote("MacArthur Foundation"),  # donor
                mysql_quote(row['grantee']),  # donee
                amount,  # amount
                mysql_quote(donation_date),  # donation_date
                mysql_quote("year"),  # donation_date_precision
                mysql_quote("donation log"),  # donation_date_basis
                mysql_quote("FIXME"),  # cause_area
                mysql_quote("https://www.macfound.org/grants/"),  # url
                mysql_quote("FIXME"),  # donor_cause_area_url
                mysql_quote(row['notes']),  # notes
                mysql_quote("FIXME"),  # affected_countries
                mysql_quote(row['location']),  # affected_regions
            ]) + ")")
            first = False
        print(";")


if __name__ == "__main__":
    main()
