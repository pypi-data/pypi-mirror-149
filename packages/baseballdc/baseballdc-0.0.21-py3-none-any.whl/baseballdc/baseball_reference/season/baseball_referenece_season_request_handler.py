import pandas as pd
from ..const import baseball_reference_season_tables_const
from ..shared import table_config_service, table_format_service, table_request_service
from ..season import season_url_service

def get_baseball_reference_season_data(query_params):

    table_configs = baseball_reference_season_tables_const.BASEBALL_REFERENCE_SEASON_TABLE_CONFIGS
    table_config = table_config_service.get_table_config(query_params, table_configs)

    url = season_url_service.construct_url(table_config, query_params)

    table = table_request_service.get_table(table_config, url, query_params)

    df = pd.read_html(str(table))[0]

    formatted_df = table_format_service.format_df(df, table_config)

    return formatted_df
