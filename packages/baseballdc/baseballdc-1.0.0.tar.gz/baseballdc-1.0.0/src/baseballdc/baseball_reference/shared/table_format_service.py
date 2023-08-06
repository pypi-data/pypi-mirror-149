def format_df(df, table_config):
    df = remove_duplicate_table_headers(df, table_config)

    return df

def remove_duplicate_table_headers(df, table_config):

    remove_rows_on = table_config['remove_rows_on']

    for entry in remove_rows_on:
        first_value = entry.partition(":")[0]
        second_value = entry.partition(":")[2]

        df = df.drop(df[df[first_value] == second_value].index)

    return df