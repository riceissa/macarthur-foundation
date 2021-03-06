#!/usr/bin/env python3
# License: CC0 https://creativecommons.org/publicdomain/zero/1.0/

import csv
import re
import sys


# In the following two lists (US_STATES and US_STATE_ABBREVS), the indexes of
# the corresponding states must match.  For example if 'California' is index 4
# in the former list, then 'CA' must also be index 4 in the latter list.
US_STATES = [
    'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut',
    'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana',
    'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts',
    'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska',
    'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina',
    'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island',
    'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont',
    'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming',
]

US_STATE_ABBREVS = [
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT",
    "DE", "FL", "GA", "HI", "ID", "IL", "IN",
    "IA", "KS", "KY", "LA", "ME", "MD", "MA",
    "MI", "MN", "MS", "MO", "MT", "NE",
    "NV", "NH", "NJ", "NM", "NY", "NC",
    "ND", "OH", "OK", "OR", "PA", "RI",
    "SC", "SD", "TN", "TX", "UT", "VT",
    "VA", "WA", "WV", "WI", "WY",
]

# From https://raw.githubusercontent.com/umpirsky/country-list/master/data/en_US/country.txt
COUNTRIES = [
    'Afghanistan', 'Åland Islands', 'Albania', 'Algeria', 'American Samoa',
    'Andorra', 'Angola', 'Anguilla', 'Antarctica', 'Antigua & Barbuda',
    'Argentina', 'Armenia', 'Aruba', 'Ascension Island', 'Australia',
    'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh',
    'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bermuda',
    'Bhutan', 'Bolivia', 'Bosnia & Herzegovina', 'Botswana', 'Brazil',
    'British Indian Ocean Territory', 'British Virgin Islands',
    'Brunei', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cambodia',
    'Cameroon', 'Canada', 'Canary Islands', 'Cape Verde', 'Caribbean Netherlands',
    'Cayman Islands', 'Central African Republic', 'Ceuta & Melilla', 'Chad',
    'Chile', 'China', 'Christmas Island', 'Cocos (Keeling) Islands',
    'Colombia', 'Comoros', 'Congo - Brazzaville', 'Congo - Kinshasa',
    'Cook Islands', 'Costa Rica', 'Côte d’Ivoire', 'Croatia', 'Cuba',
    'Curaçao', 'Cyprus', 'Czechia', 'Czech Republic', 'Denmark', 'Diego Garcia', 'Djibouti',
    'Dominica', 'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador',
    'Equatorial Guinea', 'Eritrea', 'Estonia', 'Ethiopia', 'Eurozone',
    'Falkland Islands', 'Faroe Islands', 'Fiji', 'Finland', 'France',
    'French Guiana', 'French Polynesia', 'French Southern Territories',
    'Gabon', 'The Gambia', 'Georgia', 'Germany', 'Ghana', 'Gibraltar',
    'Greece', 'Greenland', 'Grenada', 'Guadeloupe', 'Guam', 'Guatemala',
    'Guernsey', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Honduras',
    'Hong Kong SAR China', 'Hungary', 'Iceland', 'India', 'Indonesia',
    'Iran', 'Iraq', 'Ireland', 'Isle of Man', 'Israel', 'Italy', 'Jamaica',
    'Japan', 'Jersey', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', 'Kosovo',
    'Kuwait', 'Kyrgyzstan', 'Laos', 'Latvia', 'Lebanon', 'Lesotho', 'Liberia',
    'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Macau SAR China',
    'Macedonia', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali',
    'Malta', 'Marshall Islands', 'Martinique', 'Mauritania', 'Mauritius',
    'Mayotte', 'Mexico', 'Micronesia', 'Moldova', 'Monaco', 'Mongolia',
    'Montenegro', 'Montserrat', 'Morocco', 'Mozambique', 'Myanmar (Burma)',
    'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'New Caledonia', 'New Zealand',
    'Nicaragua', 'Niger', 'Nigeria', 'Niue', 'Norfolk Island', 'North Korea',
    'Northern Mariana Islands', 'Norway', 'Oman', 'Pakistan', 'Palau',
    'Palestinian Territories', 'Panama', 'Papua New Guinea', 'Paraguay',
    'Peru', 'Philippines', 'Pitcairn Islands', 'Poland', 'Portugal',
    'Puerto Rico', 'Qatar', 'Réunion', 'Romania', 'Russia', 'Rwanda',
    'Samoa', 'San Marino', 'São Tomé & Príncipe', 'Saudi Arabia',
    'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone', 'Singapore',
    'Sint Maarten', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia',
    'South Africa', 'South Georgia & South Sandwich Islands', 'South Korea',
    'South Sudan', 'Spain', 'Sri Lanka', 'St. Barthélemy', 'St. Helena',
    'St. Kitts & Nevis', 'St. Lucia', 'St. Martin', 'St. Pierre & Miquelon',
    'St. Vincent & Grenadines', 'Sudan', 'Suriname', 'Svalbard & Jan Mayen',
    'Swaziland', 'Sweden', 'Switzerland', 'Syria', 'Taiwan', 'Tajikistan',
    'Tanzania', 'Thailand', 'Timor-Leste', 'Togo', 'Tokelau', 'Tonga',
    'Trinidad and Tobago', 'Tristan da Cunha', 'Tunisia', 'Turkey',
    'Turkmenistan', 'Turks & Caicos Islands', 'Tuvalu', 'U.S. Outlying Islands',
    'US Virgin Islands', 'Uganda', 'Ukraine', 'United Arab Emirates',
    'United Kingdom', 'United Nations', 'United States', 'Uruguay',
    'Uzbekistan', 'Vanuatu', 'Vatican City', 'Venezuela', 'Vietnam',
    'Wallis & Futuna', 'Western Sahara', 'Yemen', 'Zambia', 'Zimbabwe',
]

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
    if len(sys.argv) != 1+1:
        print("Please include the input CSV file as argument one.",
              file=sys.stderr)
        sys.exit()
    with open(sys.argv[1], "r") as f:
        reader = csv.DictReader(f)
        first = True

        print("""insert into donations (donor, donee, amount, donation_date,
        donation_date_precision, donation_date_basis, cause_area, url,
        donor_cause_area_url, notes, affected_countries, affected_states,
        affected_cities, affected_regions) values""")

        for row in reader:
            amount = row['amount']
            assert amount.startswith("$")
            amount = amount.replace("$", "").replace(",", "")
            donation_date = row['date']
            assert (len(donation_date) == 4 and
                    re.match(r'^\d\d\d\d$', donation_date) is not None)
            donation_date += "-01-01"

            (affected_countries, affected_states, affected_cities,
             affected_regions) = affected_locations(row['location'])

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
                mysql_quote(affected_countries),  # affected_countries
                mysql_quote(affected_states),  # affected_states
                mysql_quote(affected_cities),  # affected_cities
                mysql_quote(affected_regions),  # affected_regions
            ]) + ")")
            first = False
        print(";")


def affected_locations(location):
    """Return a tuple (affected_countries, affected_states, affected_cities,
    affected_regions)"""
    parts = location.split(", ")
    if parts == [""]:
        return ("", "", "", "")
    if parts[-2:] == ["Korea", "South"]:
        assert len(parts) == 3, parts
        return ("South Korea", "", parts[0], "")
    if parts == ['Onike', 'Yaba', 'Lagos State', 'Nigeria']:
        return ("Nigeria", "Lagos State", "Lagos", "")
    if parts == ['Utako', 'Abuja', 'Nigeria']:
        return ("Nigeria", "Federal Capital Territory", "Abuja", "")
    if parts == ['Alto-Porvorim', 'Bardez', 'India']:
        return ("India", "Goa", "Alto-Porvorim", "")
    if parts == ['Goroka', 'EHP', 'Papua New Guinea']:
        return ("Papua New Guinea", "Eastern Highlands Province",
                "Goroka", "")
    if parts == ['Varvarino', 'Voronezh Region', 'Russia']:
        return ("Russia", "Voronezh Oblast", "Voronezh", "")
    if parts == ['Cali', 'Valle', 'Colombia']:
        return ("Colombia", "Valle del Cauca", "Santiago de Cali", "")
    if parts == ['Dzorwulu', 'Accra', 'Ghana']:
        return ("Ghana", "Accra Metropolis District", "Dzorwulu", "")
    if parts == ['Cantonments', 'Accra', 'Ghana']:
        return ("Ghana", "Accra Metropolis District", "Accra", "")
    if parts[-2:] == ['Congo', 'Democratic Republic of the']:
        assert len(parts) == 3, parts
        return ("Democratic Republic of the Congo", "", parts[0], "")
    if parts[-1] in ["D.C.", "District of Columbia"]:
        return ("United States", "", "Washington, D.C.", "")
    if parts == ['Chicago', '']:
        return ("United States", "Illinois", "Chicago", "")
    if parts[-1] in US_STATES:
        assert len(parts) == 2, parts
        return ("United States", parts[1], parts[0], "")
    if parts[-1] in US_STATE_ABBREVS:
        assert len(parts) == 2, parts
        state_name = US_STATES[US_STATE_ABBREVS.index(parts[1])]
        return ("United States", state_name, parts[0], "")
    if parts[-1] in COUNTRIES:
        if len(parts) == 1:
            return (parts[0], "", "", "")
        if len(parts) == 2:
            return (parts[1], "", parts[0], "")
        print("Not 1 or 2:", parts, file=sys.stderr)
        raise ValueError
    print("Not country or state:", parts, file=sys.stderr)
    raise ValueError

if __name__ == "__main__":
    main()
