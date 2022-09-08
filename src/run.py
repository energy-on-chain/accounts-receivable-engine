###############################################################################
# PROJECT: Accounts Receivable Engine
# AUTHOR: Matt Hartigan
# DATE: 24-August-2022
# FILENAME: run.py
# DESCRIPTION: Main entry point for the application. Coordinates input 
# processing, accessing of historical data, application of business logic, and
# auto-sending of emails.
###############################################################################
import os
import datetime
import pandas as pd 
from sqlalchemy.orm import sessionmaker

from config import params
from db import db_init, ClientStatus, ClientContactInfo, ClientContactHistory, AgingReport
from utils import process_aging_report, process_contact_info


# AUTHENTICATE
# FIXME: creds and secrets go here


# PROCESS DATA
engine = db_init()    # connect to database
session = sessionmaker(bind=engine)

date_processed = datetime.date.today()    # identify the current time at time of processing

for filename in os.listdir(params['input_data_file_path']):    # FIXME: convert to cloud folder drop

    if 'Contact' in filename:    # assumes the contact info in cloud folder is latest, drop current table and replace 
        print('Processing {}...'.format(filename))
        new_contact_info_df = process_contact_info(pd.read_excel(params['input_data_file_path'] + filename))
        new_contact_info_df.columns = ['client_id', 'name', 'email', 'phone']    # format columns properly for db commit
        new_contact_info_df.to_sql('ClientContactInfo', con=engine, if_exists='replace', index=False)

    elif 'AR' in filename:  # identify whether anynew aging reports need to be processed
        print('Processing {}...'.format(filename))
        # if AR doesn't exist... (based on filename...)
            # create new AR record
            # for every row in AR... create a ClientStatus and save

    else:
        print('The file {} was not recognized and was not processed.')


# APPLY LOGIC
# FIXME: go through AR database and pick the most current one to dictate who gets contacted how
# FIXME: remove all rows where current ending balance < 0 (we only want people who owe)
# FIXME: sort by 30 (bucket A), 60 (bucket B), 90 (bucket C), 120+ (bucket D) days late
# FIXME: each bucket has a weekly contact frequency (e.g. X times on X days). assign contact y/n and script template based on this


# MAKE CONTACT
# FIXME: get what day of the week it is (this runs daily on cloud). filter by what contacts are required
# FIXME: for every required contact, build the contact from template (e.g. include beg bal, invoice, receipt, etc. breakdown) and make it
# FIXME: compute metrics and save results


# TODO
# process aging reports
# use contact logic to process latest db aging report from list
# implement auto email contact (write email scripts)
# transfer to cloud (run every day at X AM... search cloud storage for latest AR file... process to update contact history, etc..., if no problems just keep going on last one)
# testing... (multiple AR's, duplicate clients, dropping files into the cloud, etc.)
# create dashboard... (react? sheets? what metrics?)
# write the readme

