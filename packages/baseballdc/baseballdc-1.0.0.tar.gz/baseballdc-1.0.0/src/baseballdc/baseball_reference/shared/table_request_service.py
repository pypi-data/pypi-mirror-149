import requests
from bs4 import BeautifulSoup, Comment

def get_table(table_config, url, query_params):
    response = requests.get(url, headers = {
        'accept-language':'en-US,en;q=0.8',
    })

    table = None

    table = get_commented_table(response, table_config)
    if(table == None):
        table = get_uncommented_table(response, table_config)
    
    if(table == None):
        raise ValueError(generate_table_error_message(query_params))

    return table
    

def get_uncommented_table(response, table_config):

    soup = BeautifulSoup(response.content, 'html5lib')

    table = soup.find('table', {'id': table_config['table_identifier']})

    return table


def get_commented_table(response, table_config):

    soup = BeautifulSoup(response.content, 'html5lib')

    id_plus_table_name = "".join(['id="', table_config['table_identifier'], '"'])

    commented_table = None;
    for comment in soup.findAll(text=lambda text:isinstance(text, Comment)):

        if(id_plus_table_name in comment):
            commented_table = comment

    if(commented_table != None):
        soup = BeautifulSoup(commented_table , 'html5lib')

        table = soup.find('table', {'id': table_config['table_identifier']})

        return table
    else:
        return None

def generate_table_error_message(query_params): 

    requested_table = query_params['table']
    requested_scope = query_params['scope']

    error_message_text = 'Value error in the incoming request payload:'
    data_source_error_text = f'The table requested ("{requested_table}") could not be found in the {requested_scope} scope.'
    report_text = f'If you believe this to be an error, please report this as an issue @ https://github.com/joesmi9/baseballdc.'

    return f'{error_message_text}\n\n{data_source_error_text}\n{report_text}\n';