import sys
import os

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")

import baseballdc
import unittest

class TestBaseballReferenceTeam(unittest.TestCase):

    def test_active_franchises(self):

        baseballdc_request = {
            'data_source': 'BASEBALL_REFERENCE',
            'query_params': {
                'scope': 'TEAM',
                'table': 'Active Franchises',
            }
        }

        df = baseballdc.get_data(baseballdc_request)
        df_columns = list(df.columns.values)

        expected_columns = ['Rk', 'Franchise', 'From', 'To', 'G', 'W', 'L', 'W-L%', 'G>.500', 'Divs', 'Pnnts', 'WS', 'Playoffs', 
                            'Players', 'HOF#', 'R', 'AB', 'H', 'HR', 'BA', 'RA', 'ERA']
        self.assertEqual(df_columns, expected_columns)

    def test_inactive_franchises(self):

        baseballdc_request = {
            'data_source': 'BASEBALL_REFERENCE',
            'query_params': {
                'scope': 'TEAM',
                'table': 'Inactive Franchises',
            }
        }

        df = baseballdc.get_data(baseballdc_request)
        df_columns = list(df.columns.values)

        expected_columns = ['Rk', 'Franchise', 'From', 'To', 'G', 'W', 'L', 'W-L%', 'G>.500', 'Divs', 'Pnnts', 'WS', 'Playoffs', 
                            'Players', 'HOF#', 'R', 'AB', 'H', 'HR', 'BA', 'RA', 'ERA']
        self.assertEqual(df_columns, expected_columns)

    def test_national_association_franchises(self):

        baseballdc_request = {
            'data_source': 'BASEBALL_REFERENCE',
            'query_params': {
                'scope': 'TEAM',
                'table': 'National Association Franchises',
            }
        }

        df = baseballdc.get_data(baseballdc_request)
        df_columns = list(df.columns.values)

        expected_columns = ['Rk', 'Franchise', 'From', 'To', 'G', 'W', 'L', 'W-L%', 'G>.500', 'Divs', 'Pnnts', 'WS', 'Playoffs', 
                            'Players', 'HOF#', 'R', 'AB', 'H', 'HR', 'BA', 'RA', 'ERA']
        self.assertEqual(df_columns, expected_columns)

    def test_franchise_history_table(self):

        baseballdc_request = {
            'data_source': 'BASEBALL_REFERENCE',
            'query_params': {
                'scope': 'TEAM',
                'table': 'Franchise History',
                'team': 'DET'
            }
        }

        df = baseballdc.get_data(baseballdc_request)
        df_columns = list(df.columns.values)

        expected_columns = ['Year', 'Tm', 'Lg', 'G', 'W', 'L', 'Ties', 'W-L%', 'pythW-L%', 'Finish', 'GB', 'Playoffs', 'R', 'RA', 'Attendance', 
                            'BatAge', 'PAge', '#Bat', '#P', 'Top Player', 'Managers']
        self.assertEqual(df_columns, expected_columns)


    def test_team_batting(self):

        baseballdc_request = {
            'data_source': 'BASEBALL_REFERENCE',
            'query_params': {
                'scope': 'TEAM',
                'table': 'Team Batting',
                'team': 'DET',
                'year': '2021'
            }
        }

        df = baseballdc.get_data(baseballdc_request)
        df_columns = list(df.columns.values)

        expected_columns = ['Rk', 'Pos', 'Name', 'Age', 'G', 'PA', 'AB', 'R', 'H', '2B', '3B', 'HR', 'RBI', 'SB', 'CS', 'BB', 'SO', 'BA', 'OBP', 
                            'SLG', 'OPS', 'OPS+', 'TB', 'GDP', 'HBP', 'SH', 'SF', 'IBB']
        self.assertEqual(df_columns, expected_columns)

    def test_team_pitching(self):

        baseballdc_request = {
            'data_source': 'BASEBALL_REFERENCE',
            'query_params': {
                'scope': 'TEAM',
                'table': 'Team Pitching',
                'team': 'DET',
                'year': '2021'
            }
        }

        df = baseballdc.get_data(baseballdc_request)
        df_columns = list(df.columns.values)

        expected_columns = ['Rk', 'Pos', 'Name', 'Age', 'W', 'L', 'W-L%', 'ERA', 'G', 'GS', 'GF', 'CG', 'SHO', 'SV', 'IP', 'H', 'R', 'ER', 'HR',
                            'BB', 'IBB', 'SO', 'HBP', 'BK', 'WP', 'BF', 'ERA+', 'FIP', 'WHIP', 'H9', 'HR9', 'BB9', 'SO9', 'SO/W']
        self.assertEqual(df_columns, expected_columns)

    def test_full_season_roster_and_games_by_position(self):

        baseballdc_request = {
            'data_source': 'BASEBALL_REFERENCE',
            'query_params': {
                'scope': 'TEAM',
                'table': 'Full-Season Roster & Games by Position',
                'team': 'DET',
                'year': '2021'
            }
        }

        df = baseballdc.get_data(baseballdc_request)
        df_columns = list(df.columns.values)

        expected_columns = ['Name', 'Age', 'Unnamed: 2', 'B', 'T', 'Ht', 'Wt', 'DoB', 'Yrs', 'G', 'GS', 'Batting', 'Defense', 'P', 'C', '1B', '2B',
                             '3B', 'SS', 'LF', 'CF', 'RF', 'OF', 'DH', 'PH', 'PR', 'WAR', 'Salary', 'Unnamed: 28']
        self.assertEqual(df_columns, expected_columns)

    def test_coaching_staff(self):

        baseballdc_request = {
            'data_source': 'BASEBALL_REFERENCE',
            'query_params': {
                'scope': 'TEAM',
                'table': 'Coaching Staff',
                'team': 'DET',
                'year': '2021'
            }
        }

        df = baseballdc.get_data(baseballdc_request)
        df_columns = list(df.columns.values)

        expected_columns = ['Name', 'Age', 'Unnamed: 2', 'DoB', 'Role', 'Start Date', 'End Date']
        self.assertEqual(df_columns, expected_columns)

    def test_fielding_totals(self):

        baseballdc_request = {
            'data_source': 'BASEBALL_REFERENCE',
            'query_params': {
                'scope': 'TEAM',
                'table': 'Team Fielding Totals',
                'team': 'DET',
                'year': '2021'
            }
        }

        df = baseballdc.get_data(baseballdc_request)
        df_columns = list(df.columns.values)

        expected_columns = ['Name', 'Age', 'G', 'GS', 'CG', 'Inn', 'Ch', 'PO', 'A', 'E', 'DP', 'Fld%', 'Rtot',
                             'Rtot/yr', 'Rdrs', 'Rdrs/yr', 'Rgood', 'RF/9', 'RF/G', 'PB', 'WP', 'SB', 'CS', 'CS%', 'lgCS%', 
                             'PO.1', 'Pos\xa0Summary']
        self.assertEqual(df_columns, expected_columns)

    def test_team_player_value_batters(self):

        baseballdc_request = {
            'data_source': 'BASEBALL_REFERENCE',
            'query_params': {
                'scope': 'TEAM',
                'table': 'Team Player Value--Batters',
                'team': 'DET',
                'year': '2021'
            }
        }

        df = baseballdc.get_data(baseballdc_request)
        df_columns = list(df.columns.values)

        expected_columns = ['Name', 'Age', 'G', 'PA', 'Rbat', 'Rbaser', 'Rdp', 'Rfield', 'Rpos', 'RAA', 'WAA', 'Rrep', 
                            'RAR', 'WAR', 'waaWL%', '162WL%', 'oWAR', 'dWAR', 'oRAR', 'Salary', 'Acquired', 'Pos\xa0Summary']
        self.assertEqual(df_columns, expected_columns)

    def test_team_player_value_pitchers(self):

        baseballdc_request = {
            'data_source': 'BASEBALL_REFERENCE',
            'query_params': {
                'scope': 'TEAM',
                'table': 'Team Player Value--Pitchers',
                'team': 'DET',
                'year': '2021'
            }
        }

        df = baseballdc.get_data(baseballdc_request)
        df_columns = list(df.columns.values)

        expected_columns = ['Name', 'Age', 'IP', 'G', 'GS', 'R', 'RA9', 'RA9opp', 'RA9def', 'RA9role', 'RA9extras', 'PPFp', 'RA9avg',
                             'RAA', 'WAA', 'gmLI', 'WAAadj', 'WAR', 'RAR', 'waaWL%', '162WL%', 'Salary', 'Acquired']
        self.assertEqual(df_columns, expected_columns)


    def test_team_advanced_batting(self):

        baseballdc_request = {
            'data_source': 'BASEBALL_REFERENCE',
            'query_params': {
                'scope': 'TEAM',
                'table': 'Team Advanced Batting',
                'team': 'DET',
                'year': '2021'
            }
        }

        df = baseballdc.get_data(baseballdc_request)
        df_columns = list(df.columns.values)

        expected_columns = [('Unnamed: 0_level_0', 'Name'), ('Unnamed: 1_level_0', 'Age'), ('Unnamed: 2_level_0', 'PA'), ('Batting', 'rOBA'), 
                            ('Batting', 'Rbat+'), ('Batting', 'BAbip'), ('Batting', 'ISO'), ('Batting Ratios', 'HR%'), ('Batting Ratios', 'SO%'), 
                            ('Batting Ratios', 'BB%'), ('Batted Ball', 'EV'), ('Batted Ball', 'HardH%'), ('Batted Ball', 'LD%'), ('Batted Ball', 'GB%'), 
                            ('Batted Ball', 'FB%'), ('Batted Ball', 'GB/FB'), ('Batted Ball', 'Pull%'), ('Batted Ball', 'Cent%'), ('Batted Ball', 'Oppo%'), 
                            ('Win Probability', 'WPA'), ('Win Probability', 'cWPA'), ('Win Probability', 'RE24'), ('Baserunning', 'RS%'), ('Baserunning', 'SB%'), 
                            ('Baserunning', 'XBT%')]
        self.assertEqual(df_columns, expected_columns)

    def test_team_sabermetric_batting(self):

        baseballdc_request = {
            'data_source': 'BASEBALL_REFERENCE',
            'query_params': {
                'scope': 'TEAM',
                'table': 'Team Sabermetric Batting',
                'team': 'DET',
                'year': '2021'
            }
        }

        df = baseballdc.get_data(baseballdc_request)
        df_columns = list(df.columns.values)

        expected_columns = ['Name', 'Age', 'PA', 'Outs', 'RC', 'RC/G', 'AIR', 'BAbip', 'BA', 'lgBA', 'OBP', 'lgOBP', 'SLG', 'lgSLG', 'OPS', 'lgOPS', 'OPS+',
                            'OWn%', 'BtRuns', 'BtWins', 'TotA', 'SecA', 'ISO', 'PwrSpd', 'Pos\xa0Summary']
        self.assertEqual(df_columns, expected_columns)

    def test_batting_ratios(self):

        baseballdc_request = {
            'data_source': 'BASEBALL_REFERENCE',
            'query_params': {
                'scope': 'TEAM',
                'table': 'Team Batting Ratios*',
                'team': 'DET',
                'year': '2021'
            }
        }

        df = baseballdc.get_data(baseballdc_request)
        df_columns = list(df.columns.values)

        expected_columns = ['Name', 'Age', 'PA', 'HR%', 'SO%', 'BB%', 'XBH%', 'X/H%', 'SO/W', 'AB/SO', 'AB/HR', 'AB/RBI', 'GB/FB', 'GO/AO', 'IP%', 'LD%', 
                            'HR/FB', 'IF/FB']
        self.assertEqual(df_columns, expected_columns)


    def test_win_probability(self):

        baseballdc_request = {
            'data_source': 'BASEBALL_REFERENCE',
            'query_params': {
                'scope': 'TEAM',
                'table': 'Team Win Probability*',
                'team': 'DET',
                'year': '2021'
            }
        }

        df = baseballdc.get_data(baseballdc_request)
        df_columns = list(df.columns.values)

        expected_columns = ['Name', 'Age', 'IP', 'PtchR', 'PtchW', 'Plays', 'WPA', 'WPA+', 'WPA-', 'aLI', 'WPA/LI', 'Clutch', 'cWPA', 'cWPA+', 'cWPA-', 'acLI', 
                            'cClutch', 'RE24', 'REW', 'boLI', 'RE24/boLI', 'LevHi', 'LevMd', 'LevLo']
        self.assertEqual(df_columns, expected_columns)


    def test_team_baserunning_misc(self):

        baseballdc_request = {
            'data_source': 'BASEBALL_REFERENCE',
            'query_params': {
                'scope': 'TEAM',
                'table': 'Team Baserunning/Misc*',
                'team': 'DET',
                'year': '2021'
            }
        }

        df = baseballdc.get_data(baseballdc_request)
        df_columns = list(df.columns.values)

        expected_columns = ['Name', 'Age', 'PA', 'ROE', 'XI', 'RS%', 'SBO', 'SB', 'CS', 'SB%', 'SB2', 'CS2', 'SB3', 'CS3', 'SBH', 'CSH', 'PO', 'PCS', 'OOB', 
                            'OOB1', 'OOB2', 'OOB3', 'OOBHm', 'BT', 'XBT%', '1stS', '1stS2', '1stS3', '1stD', '1stD3', '1stDH', '2ndS', '2ndS3', '2ndSH']
        self.assertEqual(df_columns, expected_columns)

    def test_team_PH_HR_situ_hitting(self):

        baseballdc_request = {
            'data_source': 'BASEBALL_REFERENCE',
            'query_params': {
                'scope': 'TEAM',
                'table': 'Team PH/HR/Situ Hitting*',
                'team': 'DET',
                'year': '2021'
            }
        }

        df = baseballdc.get_data(baseballdc_request)
        df_columns = list(df.columns.values)

        expected_columns = [('Unnamed: 0_level_0', 'Name'), ('Unnamed: 1_level_0', 'Age'), ('Unnamed: 2_level_0', 'PA'), ('Unnamed: 3_level_0', 'Ptn%'), ('Hits', 'H'),
                            ('Hits', 'Inf'), ('Hits', 'Bnt'), ('Pinch Hitting', 'AB'), ('Pinch Hitting', 'H'), ('Pinch Hitting', 'HR'), ('Pinch Hitting', 'RBI'), 
                            ('Pinch Hitting', 'PHlev'), ('Home Runs', 'All'), ('Home Runs', 'GS'), ('Home Runs', 'GSo'), ('Home Runs', 'vRH'), ('Home Runs', 'vLH'), 
                            ('Home Runs', 'Hm'), ('Home Runs', 'Rd'), ('Home Runs', 'IP'), ('SH', 'Att'), ('SH', 'Suc'), ('SH', '%'), ('GIDP', 'Opp'), ('GIDP', 'DP'), 
                            ('GIDP', '%'), ('PrdOut', 'Opp'), ('PrdOut', 'Suc'), ('PrdOut', '%'), ('BaseRunners', 'BR'), ('BaseRunners', 'BRS'), ('BaseRunners', 'BRS%'), 
                            ('Advances', '<2,3B'), ('Advances', 'Scr'), ('Advances', '%'), ('Advances', '0,2B'), ('Advances', 'Adv'), ('Advances', '%.1'), ('Unnamed: 38_level_0', 'PAu')]
        self.assertEqual(df_columns, expected_columns)

    def test_team_pitches_batting(self):

        baseballdc_request = {
            'data_source': 'BASEBALL_REFERENCE',
            'query_params': {
                'scope': 'TEAM',
                'table': 'Team Pitches Batting*',
                'team': 'DET',
                'year': '2021'
            }
        }

        df = baseballdc.get_data(baseballdc_request)
        df_columns = list(df.columns.values)

        expected_columns = ['Name', 'Age', 'PA', 'Pit', 'Pit/PA', 'Str', 'Str%', 'L/Str', 'S/Str', 'F/Str', 'I/Str', 'AS/Str', 'I/Bll', 'AS/Pit', 'Con', '1stS', '30%', '30c', '30s', 
                            '20%', '20c', '20s', '31%', '31c', '31s', 'L/SO', 'S/SO', 'L/SO%', 'PAu', 'Pitu', 'Stru']
        self.assertEqual(df_columns, expected_columns)

    def test_team_neutralized_batting(self):

        baseballdc_request = {
            'data_source': 'BASEBALL_REFERENCE',
            'query_params': {
                'scope': 'TEAM',
                'table': 'Team Neutralized Batting',
                'team': 'DET',
                'year': '2021'
            }
        }

        df = baseballdc.get_data(baseballdc_request)
        df_columns = list(df.columns.values)

        expected_columns = ['Name', 'Age', 'G', 'PA', 'AB', 'R', 'H', '2B', '3B', 'HR', 'RBI', 'SB', 'CS', 'BB', 'SO', 'BA', 'OBP', 'SLG', 'OPS', 'RC', 'Gact']
        self.assertEqual(df_columns, expected_columns)

    def test_team_cumulative_batting(self):

        baseballdc_request = {
            'data_source': 'BASEBALL_REFERENCE',
            'query_params': {
                'scope': 'TEAM',
                'table': 'Team Cumulative Batting',
                'team': 'DET',
                'year': '2021'
            }
        }

        df = baseballdc.get_data(baseballdc_request)
        df_columns = list(df.columns.values)

        expected_columns = ['Name', 'Age', 'Yrs', 'G', 'PA', 'AB', 'R', 'H', '2B', '3B', 'HR', 'RBI', 'SB', 'CS', 'BB', 'SO', 'BA', 'OBP', 'SLG', 'OPS', 'OPS+',
                            'TB', 'GDP', 'HBP', 'SH', 'SF', 'IBB']
        self.assertEqual(df_columns, expected_columns)

    def test_team_advanced_pitching(self):

        baseballdc_request = {
            'data_source': 'BASEBALL_REFERENCE',
            'query_params': {
                'scope': 'TEAM',
                'table': 'Team Advanced Pitching',
                'team': 'DET',
                'year': '2021'
            }
        }

        df = baseballdc.get_data(baseballdc_request)
        df_columns = list(df.columns.values)

        expected_columns = [('Unnamed: 0_level_0', 'Name'), ('Unnamed: 1_level_0', 'Age'), ('Batting Against', 'BA'), ('Batting Against', 'OBP'), 
                            ('Batting Against', 'SLG'), ('Batting Against', 'OPS'), ('Batting Against', 'BAbip'), ('Pitching Ratios', 'HR%'), 
                            ('Pitching Ratios', 'SO%'), ('Pitching Ratios', 'BB%'), ('Batted Ball', 'EV'), ('Batted Ball', 'HardH%'), ('Batted Ball', 'LD%'), 
                            ('Batted Ball', 'GB%'), ('Batted Ball', 'FB%'), ('Batted Ball', 'GB/FB'), ('Win Probability', 'WPA'), ('Win Probability', 'cWPA'), 
                            ('Win Probability', 'RE24')]
        self.assertEqual(df_columns, expected_columns)


    def test_team_pitching_ratios(self):

        baseballdc_request = {
            'data_source': 'BASEBALL_REFERENCE',
            'query_params': {
                'scope': 'TEAM',
                'table': 'Team Pitching Ratios*',
                'team': 'DET',
                'year': '2021'
            }
        }

        df = baseballdc.get_data(baseballdc_request)
        df_columns = list(df.columns.values)

        expected_columns = ['Name', 'Age', 'IP', 'Ptn%', 'HR%', 'SO%', 'BB%', 'SO-BB%', 'XBH%', 'X/H%', 'GB/FB', 'GO/AO', 'IP%', 'LD%', 'HR/FB', 'IF/FB', 'Opp', 'DP', '%', 'PAu']
        self.assertEqual(df_columns, expected_columns)


    def test_team_batting_against(self):

        baseballdc_request = {
            'data_source': 'BASEBALL_REFERENCE',
            'query_params': {
                'scope': 'TEAM',
                'table': 'Team Batting Against*',
                'team': 'DET',
                'year': '2021'
            }
        }

        df = baseballdc.get_data(baseballdc_request)
        df_columns = list(df.columns.values)

        expected_columns = ['Name', 'Age', 'IP', 'PAu', 'G', 'PA', 'AB', 'R', 'H', '2B', '3B', 'HR', 'SB', 'CS', 'BB', 'SO', 'BA', 'OBP', 
                            'SLG', 'OPS', 'BAbip', 'TB', 'GDP', 'HBP', 'SH', 'SF', 'IBB', 'ROE']
        self.assertEqual(df_columns, expected_columns)

    def test_team_win_probability(self):

        baseballdc_request = {
            'data_source': 'BASEBALL_REFERENCE',
            'query_params': {
                'scope': 'TEAM',
                'table': 'Team Win Probability*',
                'team': 'DET',
                'year': '2021'
            }
        }

        df = baseballdc.get_data(baseballdc_request)
        df_columns = list(df.columns.values)

        expected_columns =['Name', 'Age', 'IP', 'PtchR', 'PtchW', 'Plays', 'WPA', 'WPA+', 'WPA-', 'aLI', 'WPA/LI', 'Clutch', 'cWPA', 'cWPA+', 
                           'cWPA-', 'acLI', 'cClutch', 'RE24', 'REW', 'boLI', 'RE24/boLI', 'LevHi', 'LevMd', 'LevLo']
        self.assertEqual(df_columns, expected_columns)


    def test_team_standard_pitching(self):

        baseballdc_request = {
            'data_source': 'BASEBALL_REFERENCE',
            'query_params': {
                'scope': 'TEAM',
                'table': 'Team Starting Pitching*',
                'team': 'DET',
                'year': '2021'
            }
        }

        df = baseballdc.get_data(baseballdc_request)
        df_columns = list(df.columns.values)

        expected_columns = ['Name', 'Age', 'IP', 'G', 'GS', 'Wgs', 'Lgs', 'ND', 'Wchp', 'Ltuf', 'Wtm', 'Ltm', 'tmW-L%', 'Wlst', 'Lsv', 'CG', 
                            'SHO', 'QS', 'QS%', 'GmScA', 'Best', 'Wrst', 'BQR', 'BQS', 'sDR', 'lDR', 'RS/GS', 'RS/IP', 'IP/GS', 'Pit/GS', '<80', 
                            '80-99', '100-119', '≥120', 'Max']
        self.assertEqual(df_columns, expected_columns)


    def test_team_relief_pitching(self):

        baseballdc_request = {
            'data_source': 'BASEBALL_REFERENCE',
            'query_params': {
                'scope': 'TEAM',
                'table': 'Team Relief Pitching*',
                'team': 'DET',
                'year': '2021'
            }
        }

        df = baseballdc.get_data(baseballdc_request)
        df_columns = list(df.columns.values)

        expected_columns = ['Name', 'Age', 'IP', 'G', 'GR', 'GF', 'Wgr', 'Lgr', 'SVOpp', 'SV', 'BSv', 'SV%', 'SVSit', 'Hold', 'IR', 'IS', 'IS%', 
                            '1stIP', 'aLI', 'LevHi', 'LevMd', 'LevLo', 'Ahd', 'Tie', 'Bhd', 'Runr', 'Empt', '>3o', '<3o', 'IPmult', '0DR', 'Out/GR', 
                            'Pit/GR']
        self.assertEqual(df_columns, expected_columns)


    def test_team_baserunning_situ(self):

        baseballdc_request = {
            'data_source': 'BASEBALL_REFERENCE',
            'query_params': {
                'scope': 'TEAM',
                'table': 'Team Baserunning/Situ*',
                'team': 'DET',
                'year': '2021'
            }
        }

        df = baseballdc.get_data(baseballdc_request)
        df_columns = list(df.columns.values)

        expected_columns = ['Name', 'Age', 'IP', 'PA', 'H', 'Inf', 'Bnt', 'All', 'GS', 'GSo', 'vRH', 'vLH', 'Hm', 'Rd', '<2,3B', 'Scr', 'SO', 
                            '%', 'ROE', 'WP', 'PB', 'SBO', 'SB', 'CS', 'SB%', 'SB2', 'CS2', 'SB3', 'CS3', 'SBH', 'CSH', 'PO', 'PCS', 'BT', 'PAu']
        self.assertEqual(df_columns, expected_columns)


    def test_team_pitching_pitches(self):

        baseballdc_request = {
            'data_source': 'BASEBALL_REFERENCE',
            'query_params': {
                'scope': 'TEAM',
                'table': 'Team Pitching Pitches*',
                'team': 'DET',
                'year': '2021'
            }
        }

        df = baseballdc.get_data(baseballdc_request)
        df_columns = list(df.columns.values)

        expected_columns = ['Name', 'Age', 'IP', 'PA', 'Pit', 'Pit/PA', 'Str', 'Str%', 'L/Str', 'S/Str', 'F/Str', 'I/Str', 'AS/Str', 'I/Bll', 
                            'AS/Pit', 'Con', '1st%', '30%', '30c', '30s', '02%', '02c', '02s', '02h', 'L/SO', 'S/SO', 'L/SO%', '3pK', '4pW', 
                            'PAu', 'Pitu', 'Stru']
        self.assertEqual(df_columns, expected_columns)


    def test_team_neutralized_pitching(self):

        baseballdc_request = {
            'data_source': 'BASEBALL_REFERENCE',
            'query_params': {
                'scope': 'TEAM',
                'table': 'Team Neutralized Pitching',
                'team': 'DET',
                'year': '2021'
            }
        }

        df = baseballdc.get_data(baseballdc_request)
        df_columns = list(df.columns.values)

        expected_columns = ['Name', 'Age', 'W', 'L', 'W-L%', 'ERA', 'IP', 'H', 'R', 'ER', 'HR', 'BB', 'SO', 'HBP', 'WHIP', 'H9', 'BB9', 'SO9', 'SO/W', 'HR9', 'Unnamed: 20', 'Gact']
        self.assertEqual(df_columns, expected_columns)


    def test_team_cumulative_pitching(self):

        baseballdc_request = {
            'data_source': 'BASEBALL_REFERENCE',
            'query_params': {
                'scope': 'TEAM',
                'table': 'Team Cumulative Pitching',
                'team': 'DET',
                'year': '2021'
            }
        }

        df = baseballdc.get_data(baseballdc_request)
        df_columns = list(df.columns.values)

        expected_columns = ['Name', 'Age', 'Yrs', 'W', 'L', 'W-L%', 'ERA', 'G', 'GS', 'GF', 'CG', 'SHO', 'SV', 'IP', 'H', 'R', 'ER', 'HR', 'BB', 'IBB', 'SO', 'HBP', 'BK', 'WP', 'BF', 
                            'ERA+', 'WHIP', 'H9', 'HR9', 'BB9', 'SO9', 'SO/W', 'ERA+.1']
        self.assertEqual(df_columns, expected_columns)

if __name__ == '__main__':
        unittest.main()

