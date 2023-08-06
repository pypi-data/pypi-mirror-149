import requests
from bs4 import BeautifulSoup

def get_player_href(first_name, last_name):

    last_name_first_letter = last_name[0].lower()

    url = f'https://www.baseball-reference.com/players/{last_name_first_letter}/'

    response = requests.get(url, headers = {
        'accept-language':'en-US,en;q=0.8',
    })

    soup = BeautifulSoup(response.content, 'html5lib')

    table = soup.find('div', {'id': 'div_players_'})

    name = f'{first_name} {last_name}' 

    href = None
    for para in table.find_all("p"):
        if name.upper() in para.get_text().upper(): 
            el = para.find(href=True)
            href = el['href']

    if(href == None):
        raise ValueError(generate_player_not_found_error_message(first_name, last_name))

    return href

def generate_player_not_found_error_message(first_name, last_name): 

    error_message_text = 'Value error in the incoming request payload:'
    not_found_error_text = f'Could not find the requested player on Baseball Reference ("{first_name} {last_name}")'
    report_text = f'If you believe this to be an error, please report this as an issue @ https://github.com/joesmi9/baseballdc.'

    return f'{error_message_text}\n\n{not_found_error_text}\n{report_text}\n';