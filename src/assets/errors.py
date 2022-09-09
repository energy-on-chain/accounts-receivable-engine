from config import params

data_processing_error = {
    'subject': 'Data Error - {} Deeper Pockets Project'.format(params['client_name']),
    'body': 'There was an error while processing data for the {} Deeper Pockets Project.\n\n'.format(params['client_name']),
    'footer': 'The system was shut down.',
}

