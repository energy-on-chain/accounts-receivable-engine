import pandas as pd


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
