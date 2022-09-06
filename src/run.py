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
from sqlalchemy.orm import Session

from config import params
from db import db_init


# AUTHENTICATE
# FIXME: creds go here


# DATA
# Get New Data
year, week, day = datetime.date.today().isocalendar()    # identify the current week number
week = 34    # FIXME: dev only
raw_input_filename = [f for f in os.listdir(params['raw_input_file_path']) if str(week) in f][0]    # select the file that matches the current week
raw_input_df = pd.read_excel(params['raw_input_file_path'] + raw_input_filename)    # read in the raw data for the selected file

# Format New Data
raw_input_df = raw_input_df.drop(raw_input_df.columns[[1, 3, 5, 12]], axis=1)    # drop blank cols
raw_input_df = raw_input_df.drop([0, 1, 2, 4], axis=0)    # drop blank rows
raw_input_df = raw_input_df.reset_index(drop=True)

raw_input_df.columns = raw_input_df.iloc[0]    # rename cols
raw_input_df = raw_input_df.drop(raw_input_df.index[0])

raw_input_df['temp_name_col'] = raw_input_df['Name/Description'].shift(periods=-1)    # collapse rows with two-line names
raw_input_df['temp_name_col'] = raw_input_df['Name/Description'] + raw_input_df['temp_name_col']    # create temp col with single-line names
temp_df = pd.to_numeric(raw_input_df['ID'], errors='coerce')    # identify where two-line names are by finding ID's with no value
idx = temp_df.isna()    # convert them to nans
raw_input_df.loc[idx.shift(periods=-1) == True, 'Name/Description'] = raw_input_df['temp_name_col']    # replace the two-line names
raw_input_df['idx'] = idx
raw_input_df = raw_input_df[raw_input_df['idx'] == False]    # drop the unneeded two-line name rows
raw_input_df = raw_input_df.drop(['temp_name_col', 'idx'], axis=1)    # drop construction cols
raw_input_df = raw_input_df.reset_index(drop=True)
print(raw_input_df)

# Connect To Historical Data (from database)
engine = db_init()    # create db engine
session = Session(engine)    # create db session

# Update Historical Data
# FIXME: Create New Aging Report
# FIXME: Create New Clients
# FIXME: Update Old Clients


# LOGIC
# FIXME: remove all rows where current ending balance < 0 (we only want people who owe)
# FIXME: sort by 30 (bucket A), 60 (bucket B), 90 (bucket C), 120+ (bucket D) days late
# FIXME: each bucket has a weekly contact frequency (e.g. X times on X days). assign contact y/n and script template based on this


# CONTACT
# FIXME: get what day of the week it is (this runs daily on cloud). filter by what contacts are required
# FIXME: for every required contact, build the contact from template (e.g. include beg bal, invoice, receipt, etc. breakdown) and make it
# FIXME: compute metrics and save results


# TODO
# create initial db and update functions
# implement contact logic
# write original email and text scripts
# manually test initial contact logic
# move to cloud and dailiy repeat function (how will it look through the db initially and make contacts?)
# create dashboard for metrics, working backwards from what we want to see (react, sheets, python, etc.)
# write the readme
# write the README

