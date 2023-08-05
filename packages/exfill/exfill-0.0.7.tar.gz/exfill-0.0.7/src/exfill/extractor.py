"""grabby will scrape LinkedIn job postings, parse out details about
each posting, then combine all of the information into a single useable
csv file.
"""
import argparse
import configparser
import logging
import sys
import os

from parsers.linkedin_parser import parse_linkedin_postings
from scrapers.linkedin_scraper import scrape_linkedin_postings

def init_parser():
    """Initialize argument parser.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("site",
        choices=["linkedin"],
        help="Site to scrape")
    parser.add_argument("action",
        choices=["scrape", "parse"],
        help="Action to perform")
    return vars(parser.parse_args())

def load_config():
    """Load config file
    """
    config = configparser.ConfigParser(
      interpolation=configparser.ExtendedInterpolation())
    config.read('config.ini')

    return config

def create_dirs(config):
    """Create directories referenced in the config file
    """
    # for item in config['Directories']:
    for dir_path in config.items('Directories'):
        if not os.path.exists(dir_path[1]):
            os.mkdir(dir_path[1])

def main():
    """Main controller function used to call child functions/modules.
    """
    # Load config
    config = load_config()

    create_dirs(config)

    # Initialize logging
    log_file_name = config['Paths']['app_log']
    logging.basicConfig(
        filename=log_file_name,
        level=logging.INFO,     # level=logging.INFO should be default
        format='[%(asctime)s] [%(levelname)s] - %(message)s',
        filemode='w+')

    args = init_parser()
    logging.info('Starting app with the following input args: %s', args)

    if args["site"] == 'linkedin':
        if args["action"] == 'scrape':
            # postings_to_scrape will round up by 25 as 25
            # postings are loaded per page
            scrape_linkedin_postings(
              config,
              postings_to_scrape=5)
        if args["action"] == 'parse':
            parse_linkedin_postings(config)

    logging.info("Finished execution.  Exiting application.")
    sys.exit()

if __name__ == "__main__":

    main()
