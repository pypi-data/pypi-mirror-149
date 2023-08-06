from .team import baseball_reference_team_request_handler
from .season import baseball_referenece_season_request_handler
from .individual_player import baseball_reference_individual_player_request_handler

from .const import baseball_reference_scope_const

def get_baseball_reference_data(baseballdc_request):

    query_params = baseballdc_request['query_params'];

    validate_baseball_reference_params(query_params);

    if(query_params['scope'].upper() == baseball_reference_scope_const.INDIVIDUAL_PLAYER):
        df = baseball_reference_individual_player_request_handler.get_baseball_reference_individual_player_data(query_params)

    elif(query_params['scope'].upper() == baseball_reference_scope_const.TEAM):
        df = baseball_reference_team_request_handler.get_baseball_reference_team_data(query_params)
        
    elif(query_params['scope'].upper() == baseball_reference_scope_const.SEASON):
        df = baseball_referenece_season_request_handler.get_baseball_reference_season_data(query_params)

    return df

def validate_baseball_reference_params(baseball_reference_params):
    if(baseball_reference_params.get('scope').upper() not in baseball_reference_scope_const.BASEBALL_REFERENCE_SCOPE_LIST):
        raise ValueError(generate_scope_error_message(baseball_reference_params))


def generate_scope_error_message(baseball_reference_params): 

    requested_scope = baseball_reference_params['scope']
    valid_scopes= baseball_reference_scope_const.BASEBALL_REFERENCE_SCOPE_LIST

    error_message_text = 'Value error in the incoming request payload:'
    scope_error_text = f'The scope requested ("{requested_scope}") was not valid.'
    valid_scope_text = f'The current list of valid Baseball Reference scopes to choose from for basballdc is: {valid_scopes}'

    return f'{error_message_text}\n\n{scope_error_text}\n{valid_scope_text}\n';