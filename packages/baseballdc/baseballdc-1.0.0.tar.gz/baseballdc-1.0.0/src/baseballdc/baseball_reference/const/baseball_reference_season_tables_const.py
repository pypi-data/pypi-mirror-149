BASEBALL_REFERENCE_SEASON_URL_PREFIX = 'https://www.baseball-reference.com/leagues'

BASEBALL_REFERENCE_LEAUGE_TABLE_CONFIGS = [
    {
        'table': 'Team Wins',
        'table_identifier': 'teams_team_wins3000',
        'url_prefix': BASEBALL_REFERENCE_SEASON_URL_PREFIX,
        'league_required': True,
        'year_required': False,
        'url_postfix': '',
        'shtml_postfix_required': False,
        'remove_rows_on': []     
    }
]

BASEBALL_REFERENCE_LEAUGE_YEAR_CONFIGS = [
    {
        'table': 'East Division',
        'table_identifier': 'standings_E',
        'url_prefix': BASEBALL_REFERENCE_SEASON_URL_PREFIX,
        'league_required': True,
        'year_required': True,
        'url_postfix': '',
        'shtml_postfix_required': True,
        'remove_rows_on': []     
    },
    {
        'table': 'Central Division',
        'table_identifier': 'standings_C',
        'url_prefix': BASEBALL_REFERENCE_SEASON_URL_PREFIX,
        'league_required': True,
        'year_required': True,
        'url_postfix': '',
        'shtml_postfix_required': True,
        'remove_rows_on': []     
    },
    {
        'table': 'West Division',
        'table_identifier': 'standings_W',
        'url_prefix': BASEBALL_REFERENCE_SEASON_URL_PREFIX,
        'league_required': True,
        'year_required': True,
        'url_postfix': '',
        'shtml_postfix_required': True,
        'remove_rows_on': []     
    },
    {
        'table': 'Postseason',
        'table_identifier': 'postseason',
        'url_prefix': BASEBALL_REFERENCE_SEASON_URL_PREFIX,
        'league_required': True,
        'year_required': True,
        'url_postfix': '',
        'shtml_postfix_required': True,
        'remove_rows_on': []     
    },
    {
        'table': 'Team Standard Batting',
        'table_identifier': 'teams_standard_batting',
        'url_prefix': BASEBALL_REFERENCE_SEASON_URL_PREFIX,
        'league_required': True,
        'year_required': True,
        'url_postfix': '',
        'shtml_postfix_required': True,
        'remove_rows_on': []     
    },
    {
        'table': 'Team Standard Pitching',
        'table_identifier': 'teams_standard_pitching',
        'url_prefix': BASEBALL_REFERENCE_SEASON_URL_PREFIX,
        'league_required': True,
        'year_required': True,
        'url_postfix': '',
        'shtml_postfix_required': True,
        'remove_rows_on': []     
    },
    {
        'table': 'American League Wins Above Average By Position',
        'table_identifier': 'team_output',
        'url_prefix': BASEBALL_REFERENCE_SEASON_URL_PREFIX,
        'league_required': True,
        'year_required': True,
        'url_postfix': '',
        'shtml_postfix_required': True,
        'remove_rows_on': []     
    },
    {
        'table': 'National League Wins Above Average By Position',
        'table_identifier': 'team_output',
        'url_prefix': BASEBALL_REFERENCE_SEASON_URL_PREFIX,
        'league_required': True,
        'year_required': True,
        'url_postfix': '',
        'shtml_postfix_required': True,
        'remove_rows_on': []     
    },
    {
        'table': 'Team Fielding',
        'table_identifier': 'teams_standard_fielding',
        'url_prefix': BASEBALL_REFERENCE_SEASON_URL_PREFIX,
        'league_required': True,
        'year_required': True,
        'url_postfix': '',
        'shtml_postfix_required': True,
        'remove_rows_on': []     
    },
    {
        'table': 'Major League Baseball Wins Above Avg By Position',
        'table_identifier': 'team_output',
        'url_prefix': BASEBALL_REFERENCE_SEASON_URL_PREFIX,
        'league_required': True,
        'year_required': True,
        'url_postfix': '',
        'shtml_postfix_required': True,
        'remove_rows_on': []     
    }
]

BASEBALL_REFERENCE_LEAUGE_YEAR_STANDINGS_CONFIGS = [
    {
        'table': 'American League East Detailed Standings',
        'table_identifier': 'expanded_standings_E',
        'url_prefix': BASEBALL_REFERENCE_SEASON_URL_PREFIX,
        'league_required': True,
        'year_required': True,
        'url_postfix': '-standings',
        'shtml_postfix_required': True,
        'remove_rows_on': []     
    },
    {
        'table': 'American League Central Detailed Standings',
        'table_identifier': 'expanded_standings_C',
        'url_prefix': BASEBALL_REFERENCE_SEASON_URL_PREFIX,
        'league_required': True,
        'year_required': True,
        'url_postfix': '-standings',
        'shtml_postfix_required': True,
        'remove_rows_on': []     
    },
    {
        'table': 'American League West Detailed Standings',
        'table_identifier': 'expanded_standings_W',
        'url_prefix': BASEBALL_REFERENCE_SEASON_URL_PREFIX,
        'league_required': True,
        'year_required': True,
        'url_postfix': '-standings',
        'shtml_postfix_required': True,
        'remove_rows_on': []     
    },
    {
        'table': 'American League Wild Card Detailed Standings',
        'table_identifier': 'expanded_standings_wild_card',
        'url_prefix': BASEBALL_REFERENCE_SEASON_URL_PREFIX,
        'league_required': True,
        'year_required': True,
        'url_postfix': '-standings',
        'shtml_postfix_required': True,
        'remove_rows_on': []     
    },
    {
        'table': 'Head-To-Head Records',
        'table_identifier': 'head_to_head_wins',
        'url_prefix': BASEBALL_REFERENCE_SEASON_URL_PREFIX,
        'league_required': True,
        'year_required': True,
        'url_postfix': '-standings',
        'shtml_postfix_required': True,
        'remove_rows_on': []     
    },
    {
        'table': 'Head to Head Run Scoring',
        'table_identifier': 'head_to_head_runs',
        'url_prefix': BASEBALL_REFERENCE_SEASON_URL_PREFIX,
        'league_required': True,
        'year_required': True,
        'url_postfix': '-standings',
        'shtml_postfix_required': True,
        'remove_rows_on': []     
    },
    {
        'table': 'National League East Detailed Standings',
        'table_identifier': 'expanded_standings_E',
        'url_prefix': BASEBALL_REFERENCE_SEASON_URL_PREFIX,
        'league_required': True,
        'year_required': True,
        'url_postfix': '-standings',
        'shtml_postfix_required': True,
        'remove_rows_on': []     
    },
    {
        'table': 'National League Central Detailed Standings',
        'table_identifier': 'expanded_standings_C',
        'url_prefix': BASEBALL_REFERENCE_SEASON_URL_PREFIX,
        'league_required': True,
        'year_required': True,
        'url_postfix': '-standings',
        'shtml_postfix_required': True,
        'remove_rows_on': []     
    },
    {
        'table': 'National League West Detailed Standings',
        'table_identifier': 'expanded_standings_W',
        'url_prefix': BASEBALL_REFERENCE_SEASON_URL_PREFIX,
        'league_required': True,
        'year_required': True,
        'url_postfix': '-standings',
        'shtml_postfix_required': True,
        'remove_rows_on': []     
    },
    {
        'table': 'National League Wild Card Detailed Standings',
        'table_identifier': 'expanded_standings_wild_card',
        'url_prefix': BASEBALL_REFERENCE_SEASON_URL_PREFIX,
        'league_required': True,
        'year_required': True,
        'url_postfix': '-standings',
        'shtml_postfix_required': True,
        'remove_rows_on': []     
    }
]

BASEBALL_REFERENCE_LEAUGE_YEAR_STANDARD_FIELDING_CONFIGS = [
    {
        'table': 'Player Standard Fielding',
        'table_identifier': 'players_players_standard_fielding_fielding',
        'url_prefix': BASEBALL_REFERENCE_SEASON_URL_PREFIX,
        'league_required': True,
        'year_required': True,
        'url_postfix': '-standard-fielding',
        'shtml_postfix_required': True,
        'remove_rows_on': []     
    }
]

BASEBALL_REFERENCE_LEAUGE_YEAR_STANDARD_BATTING_CONFIGS = [
    {
        'table': 'Player Standard Batting',
        'table_identifier': 'players_standard_batting',
        'url_prefix': BASEBALL_REFERENCE_SEASON_URL_PREFIX,
        'league_required': True,
        'year_required': True,
        'url_postfix': '-standard-batting',
        'shtml_postfix_required': True,
        'remove_rows_on': []     
    }
]

BASEBALL_REFERENCE_LEAUGE_YEAR_STANDARD_PITCHING_CONFIGS = [
    {
        'table': 'Player Standard Pitching',
        'table_identifier': 'players_standard_pitching',
        'url_prefix': BASEBALL_REFERENCE_SEASON_URL_PREFIX,
        'league_required': True,
        'year_required': True,
        'url_postfix': '-standard-pitching',
        'shtml_postfix_required': True,
        'remove_rows_on': []     
    }
]

BASEBALL_REFERENCE_SEASON_TABLE_CONFIGS = [
    *BASEBALL_REFERENCE_LEAUGE_TABLE_CONFIGS,
    *BASEBALL_REFERENCE_LEAUGE_YEAR_CONFIGS,
    *BASEBALL_REFERENCE_LEAUGE_YEAR_STANDINGS_CONFIGS,
    *BASEBALL_REFERENCE_LEAUGE_YEAR_STANDARD_FIELDING_CONFIGS,
    *BASEBALL_REFERENCE_LEAUGE_YEAR_STANDARD_BATTING_CONFIGS,
    *BASEBALL_REFERENCE_LEAUGE_YEAR_STANDARD_PITCHING_CONFIGS
]