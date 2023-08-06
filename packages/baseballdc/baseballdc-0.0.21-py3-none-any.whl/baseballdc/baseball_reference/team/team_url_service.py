def construct_url(table_config, query_params):

    url_prefix = table_config['url_prefix']

    url_team = ''
    if(table_config['team_required'] == True):

        if 'team' not in query_params:
            raise ValueError(generate_team_required_error_message(query_params))

        url_team = '/' + query_params['team']

    url_year = ''
    if(table_config['year_required'] == True):

        if 'year' not in query_params:
            raise ValueError(generate_year_required_error_message(query_params))

        url_year = '/' + str(query_params['year'])

    url_postfix = table_config['url_postfix']

    shtml_postfix = ''
    if(table_config['shtml_postfix_required'] == True):
        shtml_postfix = '.shtml'

    url = f'{url_prefix}{url_team}{url_year}{url_postfix}{shtml_postfix}'

    print(f'baseballdc url: {url}')
    return url

def generate_team_required_error_message(query_params): 

    requested_table = query_params['table']

    error_message_text = 'Value error in the incoming request payload:'
    team_error_text = f'The table requested ("{requested_table}") requires a team to be specified in the query parameters.'
    report_text = f'If you believe this to be an error, please report this as an issue @ https://github.com/joesmi9/baseballdc.'

    return f'{error_message_text}\n\n{team_error_text}\n{report_text}\n';

def generate_year_required_error_message(query_params): 

    requested_table = query_params['table']

    error_message_text = 'Value error in the incoming request payload:'
    year_error_text = f'The table requested ("{requested_table}") requires a year to be specified in the query parameters.'
    report_text = f'If you believe this to be an error, please report this as an issue @ https://github.com/joesmi9/baseballdc.'

    return f'{error_message_text}\n\n{year_error_text}\n{report_text}\n';