# MacArthur Foundation

This is for Vipul Naik's [Donations List Website](https://github.com/vipulnaik/donations).

see https://github.com/vipulnaik/donations/issues/4
for the issue that initiated this repo.

see https://www.macfound.org/grants/ for the data source.

files:

- `scrape.py`: scrapes the grants info and stores it in a CSV file. Scraping takes over an hour.
- `proc.py`: takes the data stored in the CSV and transforms it into a SQL file (a SQL insert statement with a bunch of values) that can be loaded into MySQL. The schema for this is in the [donations repo](https://github.com/vipulnaik/donations).

## Instructions for doing a run

```bash
./scrape.py out.csv
./proc.py out.csv > out.sql
```

## License

CC0 for the scripts, not sure about the data.
