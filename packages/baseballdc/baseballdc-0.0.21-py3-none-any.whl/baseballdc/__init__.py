from .const import data_source_const
from .baseball_reference import baseball_referenence_request_handler
from .request_validation import request_validator
 
def get_data(baseballdc_request):

    # Validate that the incoming request payload has a valid data source.
    request_validator.validate_incoming_payload(baseballdc_request)

    # Route the request to the correct data source handler, and generate the requested dataframe
    df = route_get_data_request(baseballdc_request)

    # return dataframe
    return df

def route_get_data_request(baseballdc_request):
    requested_data_source_trimmed = baseballdc_request['data_source'].strip().upper()

    if(requested_data_source_trimmed == data_source_const.BASEBALL_REFERENCE):
        df = baseball_referenence_request_handler.get_baseball_reference_data(baseballdc_request)

    return df


# # EXAMPLE REQUEST
# baseballdc_request = {
# 	'data_source': 'BASEBALL_REFERENCE',
# 	'query_params': {
#         'scope': 'TEAM',
#         'table': 'Year-by-Year Team Pitching Ranks',
#         'team': 'DET',
#         'year': 2002
# 	}
# }

# baseballdc_request_season = {
# 	'data_source': 'BASEBALL_REFERENCE',
# 	'query_params': {
#         'scope': 'SEASON',
#         'table': 'Player Standard Pitching',
#         # 'team': 'DET',
#         'year': 2003,
#         'league': 'NL'
# 	}
# }

# baseballdc_request_player = {
# 	'data_source': 'BASEBALL_REFERENCE',
# 	'query_params': {
#         'scope': 'INDIVIDUAL_PLAYER',
#         'table': 'Standard Batting',
#         'first_name': 'Miguel',
#         'last_name': "Cabrera"
# 	}
# }

# baseballdc_request_player = {
# 	'data_source': 'BASEBALL_REFERENCE',
# 	'query_params': {
#         'scope': 'INDIVIDUAL_PLAYER',
#         'table': 'Standard Batting',
#         'first_name': 'Justin',
#         'last_name': 'Verlander'
# 	}
# }


# get_data(baseballdc_request_player)