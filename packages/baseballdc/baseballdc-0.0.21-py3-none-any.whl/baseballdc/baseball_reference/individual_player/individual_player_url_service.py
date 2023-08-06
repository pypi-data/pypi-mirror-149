from .individual_player_identifier_service import get_player_href

def construct_url(table_config, query_params):

    url_prefix = 'https://www.baseball-reference.com'

    if 'first_name' not in query_params or 'last_name' not in query_params: 
        raise ValueError(generate_name_required_error_message(query_params))

    first_name = query_params['first_name']
    last_name = query_params['last_name']

    if len(first_name) == 0 or len(first_name) == 0 : 
        raise ValueError(generate_name_required_error_message(query_params))

    player_href = get_player_href(first_name, last_name)

    url = f'{url_prefix}{player_href}'

    print(f'baseballdc url: {url}')
    return url

def generate_name_required_error_message(query_params): 

    requested_table = query_params['table']

    error_message_text = 'Value error in the incoming request payload:'
    name_error_text = f'The table requested ("{requested_table}") requires the players first name and last name to be specified in the query parameters.'
    report_text = f'If you believe this to be an error, please report this as an issue @ https://github.com/joesmi9/baseballdc.'

    return f'{error_message_text}\n\n{name_error_text}\n{report_text}\n';

