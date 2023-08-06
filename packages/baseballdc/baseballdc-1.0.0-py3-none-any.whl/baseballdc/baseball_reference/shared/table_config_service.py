def get_table_config(query_params, table_configs):

    if 'table' not in query_params:
        raise ValueError(generate_no_table_in_params_error_message(query_params))

    table_config = None
    for config in table_configs:
        if(compare_table_names(query_params['table'], config['table'])):
            table_config = config
    
    if(table_config is None):
        raise ValueError(generate_table_config_error_message(query_params))

    return table_config

def compare_table_names(user_input_value, config_value):
    user_input_value_trimmed = ''.join(e for e in user_input_value if e.isalpha()).upper()
    config_value_trimmed = ''.join(e for e in config_value if e.isalpha()).upper()

    if(user_input_value_trimmed == config_value_trimmed):
        return True
    else: 
        return False

def generate_no_table_in_params_error_message(query_params): 

    error_message_text = 'Value error in the incoming request payload:'
    query_params_error_text = f'The query parameters included in the incoming request must contain a "table" key-value pair.'

    return f'{error_message_text}\n\n{query_params_error_text}\n';

def generate_table_config_error_message(query_params): 

    requested_table = query_params['table']
    requested_scope = query_params['scope']

    error_message_text = 'Value error in the incoming request payload:'
    data_source_error_text = f'The table requested ("{requested_table}") could not be found in the {requested_scope} scope.'
    report_text = f'If you believe this to be an error, please report this as an issue @ https://github.com/joesmi9/baseballdc.'

    return f'{error_message_text}\n\n{data_source_error_text}\n{report_text}\n';