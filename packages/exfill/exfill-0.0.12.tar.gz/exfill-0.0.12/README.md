# Introduction

Job boards (like LinkedIn) can be a good source for finding job openings.  Unfortunately the search results cannot always be filtered to a usable degree.  This application lets users scrape and parse jobs with more flexability provided by the default search.

Currently only LinkedIn is supported.

# Project Structure

Directories:
- `src/exfill/parsers` - Contains parser(s)
- `src/exfill/scrapers` - Contains scraper(s)
- `src/exfill/support` 
    - Contains `geckodriver` driver for FireFox which is used by Selenium
    - Download the latest driver from the [Mozilla GeckoDriver repo in GitHub](https://github.com/mozilla/geckodriver)
- `data/html` 
    - Not in source control
    - Contains HTML elements for a specific job posting
    - Populated by a scraper
- `data/csv` 
    - Not in source control
    - Contains parsed information in a csv table
    - Populated by a parser
    - Also contains an error table
- `logs` 
    - Not in source control
    - Contains logs created during execution

## `creds.json` File

Syntax should be as follows:

```json
{
    "linkedin": {
        "username": "jay-law@gmail.com",
        "password": "password1"
    }
}
```

# Usage

There are two phase.  First is scraping the postings.  Second is parsing the scraped information.  Therefore the scraping phase must occur before the parsing phase.

## Use as Code

```bash
# Install with git
$ git clone git@github.com:jay-law/job-scraper.git

# Execute - Scrape linkedin
$ python3 src/exfill/extractor.py linkedin scrape

# Execute - Parse linkedin
$ python3 src/exfill/extractor.py linkedin parse
```

## Use as Module

```bash
# Install
$ python3 -m pip install --upgrade exfill

# Execute - Parse linkedin
$ python3 -m exfill.extractor linkedin parse
```

# Roadmap

* [ ] Write unit tests
* [ ] Improve secret handling
* [x] Add packaging
* [x] Move paths to config file
* [x] Move keyword logic
* [x] Set/include default config.ini for users installing with PIP
* [x] Add CICD
* [ ] Automate versioning