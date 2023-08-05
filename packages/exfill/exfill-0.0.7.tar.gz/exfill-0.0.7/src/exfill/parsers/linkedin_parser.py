"""Parser module will process and aggregate job posting files.
"""
import datetime
import logging
import os
import re
import pandas

from bs4 import BeautifulSoup

def export_csv(config, all_postings, all_postings_err):
    """Export all postings to CSV file
    """
    output_file = config['Parser']['linkedin_output_file']
    output_file_errors = config['Parser']['linkedin_output_file_err']

    logging.info('Exporting to %s', output_file)
    pandas.DataFrame(all_postings).to_csv(output_file, index=False)

    logging.info('Exporting errors to %s', output_file_errors)
    pandas.DataFrame(all_postings_err).to_csv(output_file_errors, index=False)

def flag_error(posting_info, error_info, err_msg):
    """Flag posting with an error
    """
    error_info['error_message'] = err_msg
    error_info['element'] = 'Element is missing'
    error_value = 'ERROR'
    posting_info['company_size'] = error_value
    posting_info['company_industry'] = error_value
    posting_info['hours'] = error_value
    posting_info['level'] = error_value
    posting_info['error_flg'] = 1

def parse_details(config, posting_file, posting_info, error_info):
    """Parse out posting details contained in an HTML file
    """
    # Use jobid as the index for dataframe
    jobid = posting_file.split('_')
    jobid = jobid[1]
    logging.info('%s - Parsing job ', jobid)
    posting_info['jobid'] = jobid
    error_info['jobid'] = jobid

    # Assume no errors
    posting_info['error_flg'] = 0

    # Create BeautifulSoup object from html element
    input_file_name = os.path.join(config['Parser']['linkedin_input_dir'], posting_file)
    with open(input_file_name, mode='r', encoding='UTF-8') as file:
        soup = BeautifulSoup(file, "html.parser")

    # Set job title
    # t-24 OR t-16 should work
    posting_info['title'] = soup.find(class_ = 't-24').text.strip()

    # Set posting url
    posting_info['posting_url'] = 'https://www.linkedin.com/jobs/view/' + jobid

    # company info
    temp_company_span = soup.select('span.jobs-unified-top-card__company-name')
    temp_company_anchor = temp_company_span[0].select('a')
    if len(temp_company_anchor) == 1:
        posting_info['company_href'] = temp_company_anchor[0]['href']
        posting_info['company_name'] = temp_company_anchor[0].text.strip()
    else:
        posting_info['company_name'] = temp_company_span[0].text.strip()


    # workplace_type. looking for remote
    # remote (f_WT=2) in url
    temp_workplace_type = soup.find(
        class_ = 'jobs-unified-top-card__workplace-type').text.strip()
    posting_info['workplace_type'] = temp_workplace_type

    # Grab hours, level, company_size, and company_industry
    # syntax should be:
    # hours · level
    # company_size · company_industry
    # some postings have errors in the syntax
    temp_company_info = soup.find_all(string=re.compile(r' · '))

    # Some elements don't always load
    if len(temp_company_info) == 0:
        logging.error('%s - See error file for more info.', jobid)
        err_msg = 'Company info does not exist or was not loaded'
        flag_error(posting_info, error_info, err_msg)

        return

    for section in temp_company_info:

        section_split = section.strip().split(' · ')
        logging.debug('%s - %s', jobid, section)

        if not len(section_split) == 2:
            logging.error('%s - See error file for more info.', jobid)
            err_msg = 'Posting info section doesnt have exactly ' \
                'two elements when splitting on \' · \''
            flag_error(posting_info, error_info, err_msg)

            continue

        if 'employees' in section:
            posting_info['company_size'] = section_split[0]
            posting_info['company_industry'] = section_split[1]

        elif 'Full-time' in section:
            posting_info['hours'] = section_split[0]
            posting_info['level'] = section_split[1]

def insert_metadata(posting_file, posting_info, error_info):
    """Insert metadata like datetime into posting info
    """
    posting_info['md_file'] = posting_file
    error_info['md_file'] = posting_file

    time_stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    posting_info['md_datetime'] = time_stamp
    error_info['md_datetime'] = time_stamp

def parse_linkedin_postings(config):
    """Main parser function that controls program flow
    """
    logging.info('Parsing linkedin')

    logging.info('Loading config')
    input_dir = config['Parser']['linkedin_input_dir']

    all_postings = []
    all_postings_err = []

    for posting_file in os.listdir(input_dir):

        posting_info = {}
        error_info = {}

        # populate above objects with posting details
        parse_details(config, posting_file, posting_info, error_info)

        # insert metadata into posting_info and error_info
        insert_metadata(posting_file, posting_info, error_info)

        all_postings.append(posting_info)
        if error_info.get('error_message'):
            all_postings_err.append(error_info)

    export_csv(config, all_postings, all_postings_err)
