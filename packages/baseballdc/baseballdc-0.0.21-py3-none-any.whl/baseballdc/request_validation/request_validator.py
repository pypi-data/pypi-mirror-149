from ..const import data_source_const

def validate_incoming_payload(baseballdc_request):

    requested_data_source_trimmed = baseballdc_request['data_source'].strip().upper()

    if(requested_data_source_trimmed not in data_source_const.DATA_SOURCE_LIST):
        raise ValueError(generate_data_source_error_message(baseballdc_request))

def generate_data_source_error_message(baseballdc_request): 

    requested_data_source = baseballdc_request['data_source']
    valid_data_sources = data_source_const.DATA_SOURCE_LIST

    error_message_text = 'Value error in the incoming request payload:'
    data_source_error_text = f'The data source requested ("{requested_data_source}") was not valid.'
    valid_data_source_text = f'The current list of valid datasources to choose from for basballdc is: {valid_data_sources}'

    return f'{error_message_text}\n\n{data_source_error_text}\n{valid_data_source_text}\n';
