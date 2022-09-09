import pandas as pd
import smtplib
import imghdr
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from google.cloud import secretmanager

from config import params


def send_email_without_attachments(subject, body, footer):
    """
    Uses Gmail to send a single email to each receiver listed in the project 
    config file with the input list of attachments.
    :param subject: string, the subject line for the email
    :param subject: string, the text for the email message body
    :param subject: string, the text for the email footer
    :param attachment_path_list: list, list of string file paths to the attachments that will go on the email
    :return None
    """

    # Get secrets
    client = secretmanager.SecretManagerServiceClient()
    secret_name = "EOC_GMAIL_2FA_PASSWORD"
    request = {"name": f"projects/{params['project_id']}/secrets/{secret_name}/versions/latest"}
    response = client.access_secret_version(request)
    eoc_gmail_2fa_password = response.payload.data.decode("UTF-8")

    # Authenticate to server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(params['sender_email'], eoc_gmail_2fa_password)   

    for receiver in params['receiver_email_list']:

        # Build message
        message = MIMEMultipart()
        message['From'] = params['sender_email']
        message['To'] = receiver
        message['Subject'] = subject
        message.attach(MIMEText(body + footer, 'plain'))

        # Send message
        text = message.as_string()
        server.sendmail(params['sender_email'], receiver, text)
        print('Email sent from {} to {}'.format(params['sender_email'], receiver))

    # Shutdown server
    server.quit()


# DATA
def process_aging_report(input_df):
    """
    Reads in new aging report specified in input arguments and returns the parsed
    version ready for updating in the database.
    """

    df = input_df.copy()

    # Remove blank columns
    df = df.drop(df.columns[[1, 3, 5, 12]], axis=1)    # drop blank cols
    df = df.drop([0, 1, 2, 4], axis=0)    # drop blank rows
    df = df.reset_index(drop=True)

    # Rename columns
    df.columns = df.iloc[0]    # rename cols
    df = df.drop(df.index[0])

    # Remove two-line names
    df['temp_name_col'] = df['Name/Description'].shift(periods=-1)    # collapse rows with two-line names
    df['temp_name_col'] = df['Name/Description'] + df['temp_name_col']    # create temp col with single-line names
    temp_df = pd.to_numeric(df['ID'], errors='coerce')    # identify where two-line names are by finding ID's with no value
    idx = temp_df.isna()    # convert them to nans
    df.loc[idx.shift(periods=-1) == True, 'Name/Description'] = df['temp_name_col']    # replace the two-line names
    df['idx'] = idx
    df = df[df['idx'] == False]    # drop the unneeded two-line name rows
    df = df.drop(['temp_name_col', 'idx'], axis=1)    # drop construction cols
    df = df.reset_index(drop=True)
    df['week'] = week

    # Final column rename
    df.columns = ['client_id', 'name', 'beginning_balance', 'invoices', 'receipts', 'service_charges', 'adjustments', 'day_0_to_30', 'day_30_to_60', 'day_60_to_90', 'day_90_to_120', 'day_120_plus', 'ending_balance', 'week']

    return df


def process_contact_info(input_df):
    """
    Reads in contact info for client's accounts and returns the parsed version 
    ready for updating in the database.
    """

    df = input_df.copy()

    return df
