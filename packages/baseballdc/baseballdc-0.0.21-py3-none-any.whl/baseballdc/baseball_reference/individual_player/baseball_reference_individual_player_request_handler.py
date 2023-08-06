import pandas as pd
from ..const import baseball_reference_individual_player_tables_const
from ..shared import table_config_service, table_format_service, table_request_service
from ..individual_player import individual_player_url_service

def get_baseball_reference_individual_player_data(query_params):

    table_configs = baseball_reference_individual_player_tables_const.BASEBALL_REFERENCE_INDIVIDUAL_PLAYER_TABLE_CONFIGS
    table_config = table_config_service.get_table_config(query_params, table_configs)

    url = individual_player_url_service.construct_url(table_config, query_params)

    table = table_request_service.get_table(table_config, url, query_params)

    df = pd.read_html(str(table))[0]

    formatted_df = table_format_service.format_df(df, table_config)

    return formatted_df


