###############################################################################
# PROJECT: Accounts Receivable Engine
# AUTHOR: Matt Hartigan
# DATE: 24-August-2022
# FILENAME: config.py
# DESCRIPTION: Defines the key parameters for the codebase.
###############################################################################

params = {
    'input_data_file_path': 'src/data/',
    'database_url': 'sqlite:///hmc-sqlite.db',
    'client_name': 'Henderson Manufacturing Company',
    'project_id': 'henderson-mfg-co-360423',
    'sender_email': 'matthew@energyonchain.net',
    'receiver_email_list': [
        'matthew@smallfundsolutions.com',
        # 'matthew.t.hartigan@gmail.com',
        # 'codyacraig89@gmail.com',
    ],
}
