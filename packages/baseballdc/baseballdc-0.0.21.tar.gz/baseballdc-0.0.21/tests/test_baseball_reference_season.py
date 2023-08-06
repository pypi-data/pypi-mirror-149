import sys
import os

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")

import baseballdc
import unittest

class TestBaseballReferenceIndividualPlayer(unittest.TestCase):

    def test_team_wins(self):

        baseballdc_request = {
            'data_source': 'BASEBALL_REFERENCE',
            'query_params': {
                'scope': 'SEASON',
                'table': 'Team Wins',
                'league': 'NL',
            }
        }

        df = baseballdc.get_data(baseballdc_request)
        df_columns = list(df.columns.values)

        expected_columns = ['Year', 'G', 'ARI', 'ATL', 'CHC', 'CIN', 'COL', 'HOU', 'LAD', 'MIA', 'MIL', 'NYM', 
                            'PHI', 'PIT', 'SDP', 'SFG', 'STL', 'WSN']
        self.assertEqual(df_columns, expected_columns)

    def test_east_division(self):

        baseballdc_request = {
            'data_source': 'BASEBALL_REFERENCE',
            'query_params': {
                'scope': 'SEASON',
                'table': 'East Division',
                'league': 'NL',
                'year': '2021'
            }
        }

        df = baseballdc.get_data(baseballdc_request)
        df_columns = list(df.columns.values)

        expected_columns = ['Tm', 'W', 'L', 'W-L%', 'GB']
        self.assertEqual(df_columns, expected_columns)        

    def test_central_division(self):

        baseballdc_request = {
            'data_source': 'BASEBALL_REFERENCE',
            'query_params': {
                'scope': 'SEASON',
                'table': 'Central Division',
                'league': 'NL',
                'year': '2021'
            }
        }

        df = baseballdc.get_data(baseballdc_request)
        df_columns = list(df.columns.values)

        expected_columns = ['Tm', 'W', 'L', 'W-L%', 'GB']
        self.assertEqual(df_columns, expected_columns)  

    def test_west_division(self):

        baseballdc_request = {
            'data_source': 'BASEBALL_REFERENCE',
            'query_params': {
                'scope': 'SEASON',
                'table': 'West Division',
                'league': 'NL',
                'year': '2021'
            }
        }

        df = baseballdc.get_data(baseballdc_request)
        df_columns = list(df.columns.values)

        expected_columns = ['Tm', 'W', 'L', 'W-L%', 'GB']
        self.assertEqual(df_columns, expected_columns)  


    def test_postseason(self):

        baseballdc_request = {
            'data_source': 'BASEBALL_REFERENCE',
            'query_params': {
                'scope': 'SEASON',
                'table': 'Postseason',
                'league': 'NL',
                'year': '2021'
            }
        }

        df = baseballdc.get_data(baseballdc_request)
        df_columns = list(df.columns.values)

        expected_columns = [0, 1, 2]
        self.assertEqual(df_columns, expected_columns)  

    def test_team_standard_batting(self):

        baseballdc_request = {
            'data_source': 'BASEBALL_REFERENCE',
            'query_params': {
                'scope': 'SEASON',
                'table': 'Team Standard Batting',
                'league': 'NL',
                'year': '2021'
            }
        }

        df = baseballdc.get_data(baseballdc_request)
        df_columns = list(df.columns.values)

        expected_columns = ['Tm', '#Bat', 'BatAge', 'R/G', 'G', 'PA', 'AB', 'R', 'H', '2B', '3B', 'HR', 'RBI', 
                            'SB', 'CS', 'BB', 'SO', 'BA', 'OBP', 'SLG', 'OPS', 'OPS+', 'TB', 'GDP', 'HBP', 'SH', 
                            'SF', 'IBB', 'LOB']
        self.assertEqual(df_columns, expected_columns)  

    def test_team_standard_batting(self):

        baseballdc_request = {
            'data_source': 'BASEBALL_REFERENCE',
            'query_params': {
                'scope': 'SEASON',
                'table': 'Team Standard Pitching',
                'league': 'NL',
                'year': '2021'
            }
        }

        df = baseballdc.get_data(baseballdc_request)
        df_columns = list(df.columns.values)

        expected_columns = ['Tm', '#P', 'PAge', 'RA/G', 'W', 'L', 'W-L%', 'ERA', 'G', 'GS', 'GF', 'CG', 'tSho', 'cSho', 'SV', 
                            'IP', 'H', 'R', 'ER', 'HR', 'BB', 'IBB', 'SO', 'HBP', 'BK', 'WP', 'BF', 'ERA+', 'FIP', 'WHIP', 'H9', 
                            'HR9', 'BB9', 'SO9', 'SO/W', 'LOB']
        self.assertEqual(df_columns, expected_columns)  

    def test_american_league_wins_above_average_by_position(self):

        baseballdc_request = {
            'data_source': 'BASEBALL_REFERENCE',
            'query_params': {
                'scope': 'SEASON',
                'table': 'American League Wins Above Average By Position',
                'league': 'NL',
                'year': '2021'
            }
        }

        df = baseballdc.get_data(baseballdc_request)
        df_columns = list(df.columns.values)

        expected_columns = ['Rk', 'Total', 'All P', 'SP', 'RP', 'Non-P', 'C', '1B', '2B', '3B', 'SS', 'LF', 'CF', 'RF', 
                            'OF (All)', 'DH', 'PH']
        self.assertEqual(df_columns, expected_columns)  

    def test_national_league_wins_above_average_by_position(self):

        baseballdc_request = {
            'data_source': 'BASEBALL_REFERENCE',
            'query_params': {
                'scope': 'SEASON',
                'table': 'National League Wins Above Average By Position',
                'league': 'NL',
                'year': '2021'
            }
        }

        df = baseballdc.get_data(baseballdc_request)
        df_columns = list(df.columns.values)

        expected_columns = ['Rk', 'Total', 'All P', 'SP', 'RP', 'Non-P', 'C', '1B', '2B', '3B', 'SS', 'LF', 'CF', 'RF', 
                            'OF (All)', 'DH', 'PH']
        self.assertEqual(df_columns, expected_columns)  

    def test_team_fielding(self):

        baseballdc_request = {
            'data_source': 'BASEBALL_REFERENCE',
            'query_params': {
                'scope': 'SEASON',
                'table': 'Team Fielding',
                'league': 'NL',
                'year': '2021'
            }
        }

        df = baseballdc.get_data(baseballdc_request)
        df_columns = list(df.columns.values)

        expected_columns = ['Tm', '#Fld', 'RA/G', 'DefEff', 'G', 'GS', 'CG', 'Inn', 'Ch', 'PO', 'A', 'E', 'DP', 
                            'Fld%', 'Rtot', 'Rtot/yr', 'Rdrs', 'Rdrs/yr', 'Rgood']
        self.assertEqual(df_columns, expected_columns)  

    def test_major_league_baseball_wins_above_avg_by_position(self):

        baseballdc_request = {
            'data_source': 'BASEBALL_REFERENCE',
            'query_params': {
                'scope': 'SEASON',
                'table': 'Major League Baseball Wins Above Avg By Position',
                'league': 'NL',
                'year': '2021'
            }
        }

        df = baseballdc.get_data(baseballdc_request)
        df_columns = list(df.columns.values)

        expected_columns = ['Rk', 'Total', 'All P', 'SP', 'RP', 'Non-P', 'C', '1B', '2B', '3B', 'SS', 'LF', 
                            'CF', 'RF', 'OF (All)', 'DH', 'PH']
        self.assertEqual(df_columns, expected_columns)  

    def test_american_league_east_detailed_standings(self):

        baseballdc_request = {
            'data_source': 'BASEBALL_REFERENCE',
            'query_params': {
                'scope': 'SEASON',
                'table': 'American League East Detailed Standings',
                'league': 'AL',
                'year': '2021'
            }
        }

        df = baseballdc.get_data(baseballdc_request)
        df_columns = list(df.columns.values)

        expected_columns = ['Rk', 'Tm', 'W', 'L', 'W-L%', 'GB', 'GBsum', 'R', 'RA', 'Rdiff', 'SOS', 'SRS', 'pythWL', 
                            'Luck', 'vEast', 'vCent', 'vWest', 'Inter', 'Home', 'Road', 'ExInn', '1Run', 'vRHP', 
                            'vLHP', '≥.500', '<.500']
        self.assertEqual(df_columns, expected_columns)  

    def test_american_league_central_detailed_standings(self):

        baseballdc_request = {
            'data_source': 'BASEBALL_REFERENCE',
            'query_params': {
                'scope': 'SEASON',
                'table': 'American League Central Detailed Standings',
                'league': 'AL',
                'year': '2021'
            }
        }

        df = baseballdc.get_data(baseballdc_request)
        df_columns = list(df.columns.values)

        expected_columns = ['Rk', 'Tm', 'W', 'L', 'W-L%', 'GB', 'GBsum', 'R', 'RA', 'Rdiff', 'SOS', 'SRS', 'pythWL', 
                            'Luck', 'vEast', 'vCent', 'vWest', 'Inter', 'Home', 'Road', 'ExInn', '1Run', 'vRHP', 
                            'vLHP', '≥.500', '<.500']
        self.assertEqual(df_columns, expected_columns)  

    def test_american_league_west_detailed_standings(self):

        baseballdc_request = {
            'data_source': 'BASEBALL_REFERENCE',
            'query_params': {
                'scope': 'SEASON',
                'table': 'American League West Detailed Standings',
                'league': 'AL',
                'year': '2021'
            }
        }

        df = baseballdc.get_data(baseballdc_request)
        df_columns = list(df.columns.values)

        expected_columns = ['Rk', 'Tm', 'W', 'L', 'W-L%', 'GB', 'GBsum', 'R', 'RA', 'Rdiff', 'SOS', 'SRS', 'pythWL', 
                            'Luck', 'vEast', 'vCent', 'vWest', 'Inter', 'Home', 'Road', 'ExInn', '1Run', 'vRHP', 
                            'vLHP', '≥.500', '<.500']
        self.assertEqual(df_columns, expected_columns)  


    def test_american_league_wild_card_detailed_standings(self):

        baseballdc_request = {
            'data_source': 'BASEBALL_REFERENCE',
            'query_params': {
                'scope': 'SEASON',
                'table': 'American League Wild Card Detailed Standings',
                'league': 'AL',
                'year': '2021'
            }
        }

        df = baseballdc.get_data(baseballdc_request)
        df_columns = list(df.columns.values)

        expected_columns = ['Rk', 'Tm', 'W', 'L', 'W-L%', 'GB', 'GBsum', 'R', 'RA', 'Rdiff', 'SOS', 'SRS', 'pythWL', 
                            'Luck', 'vEast', 'vCent', 'vWest', 'Inter', 'Home', 'Road', 'ExInn', '1Run', 'vRHP', 
                            'vLHP', '≥.500', '<.500']
        self.assertEqual(df_columns, expected_columns)      

    def test_head_to_head_records(self):

        baseballdc_request = {
            'data_source': 'BASEBALL_REFERENCE',
            'query_params': {
                'scope': 'SEASON',
                'table': 'Head-To-Head Records',
                'league': 'AL',
                'year': '2021'
            }
        }

        df = baseballdc.get_data(baseballdc_request)
        df_columns = list(df.columns.values)

        expected_columns = ['Tm', 'BAL', 'BOS', 'NYY', 'TBR', 'TOR', 'CHW', 'CLE', 'DET', 'KCR', 'MIN', 'HOU', 'LAA', 
                            'OAK', 'SEA', 'TEX', 'Interleague Records']
        self.assertEqual(df_columns, expected_columns)        

    def test_head_to_head_run_scoring(self):

        baseballdc_request = {
            'data_source': 'BASEBALL_REFERENCE',
            'query_params': {
                'scope': 'SEASON',
                'table': 'Head to Head Run Scoring',
                'league': 'AL',
                'year': '2021'
            }
        }

        df = baseballdc.get_data(baseballdc_request)
        df_columns = list(df.columns.values)

        expected_columns = ['Tm', 'BAL', 'BOS', 'NYY', 'TBR', 'TOR', 'CHW', 'CLE', 'DET', 'KCR', 'MIN', 'HOU', 'LAA', 
                            'OAK', 'SEA', 'TEX', 'Interleague Records']
        self.assertEqual(df_columns, expected_columns)        

    def test_national_league_east_detailed_standings(self):

        baseballdc_request = {
            'data_source': 'BASEBALL_REFERENCE',
            'query_params': {
                'scope': 'SEASON',
                'table': 'National League East Detailed Standings',
                'league': 'NL',
                'year': '2021'
            }
        }

        df = baseballdc.get_data(baseballdc_request)
        df_columns = list(df.columns.values)

        expected_columns = ['Rk', 'Tm', 'W', 'L', 'W-L%', 'GB', 'GBsum', 'R', 'RA', 'Rdiff', 'SOS', 'SRS', 'pythWL', 'Luck', 'vEast', 'vCent', 'vWest', 'Inter', 
                            'Home', 'Road', 'ExInn', '1Run', 'vRHP', 'vLHP', '≥.500', '<.500']
        self.assertEqual(df_columns, expected_columns)        

    def test_national_league_central_detailed_standings(self):

        baseballdc_request = {
            'data_source': 'BASEBALL_REFERENCE',
            'query_params': {
                'scope': 'SEASON',
                'table': 'National League Central Detailed Standings',
                'league': 'NL',
                'year': '2021'
            }
        }

        df = baseballdc.get_data(baseballdc_request)
        df_columns = list(df.columns.values)

        expected_columns = ['Rk', 'Tm', 'W', 'L', 'W-L%', 'GB', 'GBsum', 'R', 'RA', 'Rdiff', 'SOS', 'SRS', 'pythWL', 'Luck', 'vEast', 'vCent', 'vWest', 'Inter', 
                            'Home', 'Road', 'ExInn', '1Run', 'vRHP', 'vLHP', '≥.500', '<.500']
        self.assertEqual(df_columns, expected_columns)  

    def test_national_league_west_detailed_standings(self):

        baseballdc_request = {
            'data_source': 'BASEBALL_REFERENCE',
            'query_params': {
                'scope': 'SEASON',
                'table': 'National League West Detailed Standings',
                'league': 'NL',
                'year': '2021'
            }
        }

        df = baseballdc.get_data(baseballdc_request)
        df_columns = list(df.columns.values)

        expected_columns = ['Rk', 'Tm', 'W', 'L', 'W-L%', 'GB', 'GBsum', 'R', 'RA', 'Rdiff', 'SOS', 'SRS', 'pythWL', 'Luck', 'vEast', 'vCent', 'vWest', 'Inter', 
                            'Home', 'Road', 'ExInn', '1Run', 'vRHP', 'vLHP', '≥.500', '<.500']
        self.assertEqual(df_columns, expected_columns)  


    def test_national_league_wild_card_detailed_standings(self):

        baseballdc_request = {
            'data_source': 'BASEBALL_REFERENCE',
            'query_params': {
                'scope': 'SEASON',
                'table': 'National League Wild Card Detailed Standings',
                'league': 'AL',
                'year': '2021'
            }
        }

        df = baseballdc.get_data(baseballdc_request)
        df_columns = list(df.columns.values)

        expected_columns = ['Rk', 'Tm', 'W', 'L', 'W-L%', 'GB', 'GBsum', 'R', 'RA', 'Rdiff', 'SOS', 'SRS', 'pythWL', 
                            'Luck', 'vEast', 'vCent', 'vWest', 'Inter', 'Home', 'Road', 'ExInn', '1Run', 'vRHP', 
                            'vLHP', '≥.500', '<.500']
        self.assertEqual(df_columns, expected_columns)              


    def test_player_standard_fielding(self):

        baseballdc_request = {
            'data_source': 'BASEBALL_REFERENCE',
            'query_params': {
                'scope': 'SEASON',
                'table': 'Player Standard Fielding',
                'league': 'AL',
                'year': '2021'
            }
        }

        df = baseballdc.get_data(baseballdc_request)
        df_columns = list(df.columns.values)

        expected_columns = ['Rk', 'Name', 'Age', 'Tm', 'G', 'GS', 'CG', 'Inn', 'Ch', 'PO', 'A', 'E', 'DP', 'Fld%', 
                            'Rtot', 'Rtot/yr', 'Rdrs', 'Rdrs/yr', 'Rgood', 'RF/9', 'RF/G', 'Pos\xa0Summary']
        self.assertEqual(df_columns, expected_columns)   

    def test_player_standard_batting(self):

        baseballdc_request = {
            'data_source': 'BASEBALL_REFERENCE',
            'query_params': {
                'scope': 'SEASON',
                'table': 'Player Standard Batting',
                'league': 'AL',
                'year': '2021'
            }
        }

        df = baseballdc.get_data(baseballdc_request)
        df_columns = list(df.columns.values)

        expected_columns = ['Rk', 'Name', 'Age', 'Tm', 'G', 'PA', 'AB', 'R', 'H', '2B', '3B', 'HR', 'RBI', 'SB', 'CS', 'BB', 'SO', 'BA', 
                            'OBP', 'SLG', 'OPS', 'OPS+', 'TB', 'GDP', 'HBP', 'SH', 'SF', 'IBB', 'Pos\xa0Summary']
        self.assertEqual(df_columns, expected_columns)   

    def test_player_standard_pitching(self):

        baseballdc_request = {
            'data_source': 'BASEBALL_REFERENCE',
            'query_params': {
                'scope': 'SEASON',
                'table': 'Player Standard Pitching',
                'league': 'AL',
                'year': '2021'
            }
        }

        df = baseballdc.get_data(baseballdc_request)
        df_columns = list(df.columns.values)

        expected_columns = ['Rk', 'Name', 'Age', 'Tm', 'W', 'L', 'W-L%', 'ERA', 'G', 'GS', 'GF', 'CG', 'SHO', 'SV', 'IP', 'H', 'R', 'ER', 'HR', 'BB', 'IBB', 'SO', 'HBP', 'BK', 'WP', 
                            'BF', 'ERA+', 'FIP', 'WHIP', 'H9', 'HR9', 'BB9', 'SO9', 'SO/W']
        self.assertEqual(df_columns, expected_columns)  

if __name__ == '__main__':
        unittest.main()
