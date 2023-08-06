import sys
import os

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")

import baseballdc
import unittest

class TestBaseballReferenceTeam2(unittest.TestCase):

    def test_player_standard_fielding_c(self):

        baseballdc_request = {
            'data_source': 'BASEBALL_REFERENCE',
            'query_params': {
                'scope': 'TEAM',
                'table': 'Player Standard Fielding--C',
                'year': '2021',
                'team': 'DET'
            }
        }

        df = baseballdc.get_data(baseballdc_request)
        df_columns = list(df.columns.values)

        expected_columns = ['Name', 'Age', 'G', 'GS', 'CG', 'Inn', 'Ch', 'PO', 'A', 'E', 'DP', 'Fld%', 'Rtot', 'Rtot/yr', 'Rctch', 'Rdrs', 'Rdrs/yr', 
                            'Rgood', 'Rair', 'Rrange', 'Rthrow', 'RszC', 'RsbC', 'RerC', 'RF/9', 'RF/G', 'PB', 'WP', 'SB', 'CS', 'CS%']
        self.assertEqual(df_columns, expected_columns)

    def test_player_standard_fielding_1b(self):

        baseballdc_request = {
            'data_source': 'BASEBALL_REFERENCE',
            'query_params': {
                'scope': 'TEAM',
                'table': 'Player Standard Fielding--1B',
                'year': '2021',
                'team': 'DET'
            }
        }

        df = baseballdc.get_data(baseballdc_request)
        df_columns = list(df.columns.values)

        expected_columns = ['Name', 'Age', 'G', 'GS', 'CG', 'Inn', 'Ch', 'PO', 'A', 'E', 'DP', 'Fld%', 'Rtot', 'Rtot/yr', 'Rtz', 'Rdp', 'Rdrs', 'Rdrs/yr', 
                            'Rpm', 'Rgood', 'Rair', 'Rrange', 'Rthrow', 'Rbnt', 'RF/9', 'RF/G']
        self.assertEqual(df_columns, expected_columns)

    def test_player_standard_fielding_2b(self):

        baseballdc_request = {
            'data_source': 'BASEBALL_REFERENCE',
            'query_params': {
                'scope': 'TEAM',
                'table': 'Player Standard Fielding--2B',
                'year': '2021',
                'team': 'DET'
            }
        }

        df = baseballdc.get_data(baseballdc_request)
        df_columns = list(df.columns.values)

        expected_columns = ['Name', 'Age', 'G', 'GS', 'CG', 'Inn', 'Ch', 'PO', 'A', 'E', 'DP', 'Fld%', 'Rtot', 'Rtot/yr', 'Rtz', 'Rdp', 'Rdrs', 'Rdrs/yr', 
                            'Rpm', 'Rgood', 'Rair', 'Rrange', 'Rthrow', 'Rbnt', 'RF/9', 'RF/G']
        self.assertEqual(df_columns, expected_columns)

    def test_player_standard_fielding_3b(self):

        baseballdc_request = {
            'data_source': 'BASEBALL_REFERENCE',
            'query_params': {
                'scope': 'TEAM',
                'table': 'Player Standard Fielding--3B',
                'year': '2021',
                'team': 'DET'
            }
        }

        df = baseballdc.get_data(baseballdc_request)
        df_columns = list(df.columns.values)

        expected_columns = ['Name', 'Age', 'G', 'GS', 'CG', 'Inn', 'Ch', 'PO', 'A', 'E', 'DP', 'Fld%', 'Rtot', 'Rtot/yr', 'Rtz', 'Rdp', 'Rdrs', 'Rdrs/yr', 
                            'Rpm', 'Rgood', 'Rair', 'Rrange', 'Rthrow', 'Rbnt', 'RF/9', 'RF/G']
        self.assertEqual(df_columns, expected_columns)

    def test_player_standard_fielding_ss(self):

        baseballdc_request = {
            'data_source': 'BASEBALL_REFERENCE',
            'query_params': {
                'scope': 'TEAM',
                'table': 'Player Standard Fielding--SS',
                'year': '2021',
                'team': 'DET'
            }
        }

        df = baseballdc.get_data(baseballdc_request)
        df_columns = list(df.columns.values)

        expected_columns = ['Name', 'Age', 'G', 'GS', 'CG', 'Inn', 'Ch', 'PO', 'A', 'E', 'DP', 'Fld%', 'Rtot', 'Rtot/yr', 'Rtz', 'Rdp', 'Rdrs', 'Rdrs/yr', 'Rpm', 'Rdp.1', 'Rgood', 'Rair', 'Rrange', 'Rthrow', 'RF/9', 'RF/G']
        self.assertEqual(df_columns, expected_columns)


    def test_player_standard_fielding_lf(self):

        baseballdc_request = {
            'data_source': 'BASEBALL_REFERENCE',
            'query_params': {
                'scope': 'TEAM',
                'table': 'Player Standard Fielding--LF',
                'year': '2021',
                'team': 'DET'
            }
        }

        df = baseballdc.get_data(baseballdc_request)
        df_columns = list(df.columns.values)

        expected_columns = ['Name', 'Age', 'G', 'GS', 'CG', 'Inn', 'Ch', 'PO', 'A', 'E', 'DP', 'Fld%', 'Rtot', 'Rtot/yr', 'Rtz', 'Rof', 'Rdrs', 'Rdrs/yr', 'Rpm', 'Rof.1', 'Rgood', 'RF/9', 'RF/G']
        self.assertEqual(df_columns, expected_columns)






    def test_player_standard_fielding_cf(self):

        baseballdc_request = {
            'data_source': 'BASEBALL_REFERENCE',
            'query_params': {
                'scope': 'TEAM',
                'table': 'Player Standard Fielding--CF',
                'year': '2021',
                'team': 'DET'
            }
        }

        df = baseballdc.get_data(baseballdc_request)
        df_columns = list(df.columns.values)

        expected_columns = ['Name', 'Age', 'G', 'GS', 'CG', 'Inn', 'Ch', 'PO', 'A', 'E', 'DP', 'Fld%', 'Rtot', 'Rtot/yr', 'Rtz', 'Rof', 'Rdrs', 'Rdrs/yr', 'Rpm', 'Rof.1', 'Rgood', 'RF/9', 'RF/G']
        self.assertEqual(df_columns, expected_columns)


    def test_player_standard_fielding_rf(self):

        baseballdc_request = {
            'data_source': 'BASEBALL_REFERENCE',
            'query_params': {
                'scope': 'TEAM',
                'table': 'Player Standard Fielding--RF',
                'year': '2021',
                'team': 'DET'
            }
        }

        df = baseballdc.get_data(baseballdc_request)
        df_columns = list(df.columns.values)

        expected_columns = ['Name', 'Age', 'G', 'GS', 'CG', 'Inn', 'Ch', 'PO', 'A', 'E', 'DP', 'Fld%', 'Rtot', 'Rtot/yr', 'Rtz', 'Rof', 'Rdrs', 'Rdrs/yr', 'Rpm', 'Rof.1', 'Rgood', 'RF/9', 'RF/G']
        self.assertEqual(df_columns, expected_columns)



    def test_player_standard_fielding_of(self):

        baseballdc_request = {
            'data_source': 'BASEBALL_REFERENCE',
            'query_params': {
                'scope': 'TEAM',
                'table': 'Player Standard Fielding--OF',
                'year': '2021',
                'team': 'DET'
            }
        }

        df = baseballdc.get_data(baseballdc_request)
        df_columns = list(df.columns.values)

        expected_columns = ['Name', 'Age', 'G', 'GS', 'CG', 'Inn', 'Ch', 'PO', 'A', 'E', 'DP', 'Fld%', 'Rtot', 'Rtot/yr', 'Rtz', 'Rof', 'Rdrs', 'Rdrs/yr', 'Rpm', 'Rof.1', 'Rgood', 'RF/9', 'RF/G']
        self.assertEqual(df_columns, expected_columns)


    def test_player_standard_fielding_p(self):

        baseballdc_request = {
            'data_source': 'BASEBALL_REFERENCE',
            'query_params': {
                'scope': 'TEAM',
                'table': 'Player Standard Fielding--P',
                'year': '2021',
                'team': 'DET'
            }
        }

        df = baseballdc.get_data(baseballdc_request)
        df_columns = list(df.columns.values)

        expected_columns = ['Name', 'Age', 'G', 'GS', 'CG', 'Inn', 'Ch', 'PO', 'A', 'E', 'DP', 'Fld%', 'Rdrs', 'Rdrs/yr', 'Rpm', 'Rgood', 'Rair', 'Rrange', 'Rthrow', 'RsbP', 'RF/9', 'RF/G', 'SB', 'CS', 'CS%', 'PO.1']
        self.assertEqual(df_columns, expected_columns)


    def test_player_dh_games(self):

        baseballdc_request = {
            'data_source': 'BASEBALL_REFERENCE',
            'query_params': {
                'scope': 'TEAM',
                'table': 'Player DH Games',
                'year': '2021',
                'team': 'DET'
            }
        }

        df = baseballdc.get_data(baseballdc_request)
        df_columns = list(df.columns.values)

        expected_columns = ['Name', 'Age', 'G', 'GS']
        self.assertEqual(df_columns, expected_columns)



    def test_player_advanced_fielding_c(self):

        baseballdc_request = {
            'data_source': 'BASEBALL_REFERENCE',
            'query_params': {
                'scope': 'TEAM',
                'table': 'Player Advanced Fielding -- C',
                'year': '2021',
                'team': 'DET'
            }
        }

        df = baseballdc.get_data(baseballdc_request)
        df_columns = list(df.columns.values)

        expected_columns = [('Unnamed: 0_level_0', 'Name'), ('Unnamed: 1_level_0', 'Age'), ('Unnamed: 2_level_0', 'PA'), ('Pitching Stats', 'ERA'), ('Pitching Stats', 'RA9'), ('Unnamed: 5_level_0', 'Fld'), ('Unnamed: 6_level_0', 'F2O%'), ('Unnamed: 7_level_0', 'XI'), ('Unnamed: 8_level_0', 'FC'), ('Putouts', 'Tot'), ('Putouts', 'Cgt'), ('Putouts', 'Frc'), ('Putouts', 'Tag'), ('Putouts', 'SO'), ('Assists', 'Tot'), ('Assists', '1B'), ('Assists', '2B'), ('Assists', '3B'), ('Assists', 'K23'), ('Errors', 'Tot'), ('Errors', 'Cch'), ('Errors', 'Fld'), ('Errors', 'Thr'), ('Errors', 'ROE'), ('Double Plays', 'Tot'), ('Double Plays', '263'), ('Double Plays', 'n23'), ('Double Plays', 'GB'), ('Unnamed: 28_level_0', 'bFld'), ('Unnamed: 29_level_0', 'bF2O%')]
        self.assertEqual(df_columns, expected_columns)


    def test_player_advanced_fielding_1b(self):

        baseballdc_request = {
            'data_source': 'BASEBALL_REFERENCE',
            'query_params': {
                'scope': 'TEAM',
                'table': 'Player Advanced Fielding -- 1B',
                'year': '2021',
                'team': 'DET'
            }
        }

        df = baseballdc.get_data(baseballdc_request)
        df_columns = list(df.columns.values)

        expected_columns = [('Unnamed: 0_level_0', 'Name'), ('Unnamed: 1_level_0', 'Age'), ('Unnamed: 2_level_0', 'PA'), ('Unnamed: 3_level_0', 'RHB%'), ('Unnamed: 4_level_0', 'BIP%'), ('Unnamed: 5_level_0', 'GBIP%'), ('Unnamed: 6_level_0', 'Fld'), ('Unnamed: 7_level_0', 'F2O%'), ('Unnamed: 8_level_0', 'FC'), ('Putouts', 'Tot'), ('Putouts', 'Cgt'), ('Putouts', 'Frc'), ('Putouts', 'Tag'), ('Assists', 'Tot'), ('Assists', '1B'), ('Assists', '2B'), ('Assists', 'Hm'), ('Assists', 'Rly'), ('Errors', 'Tot'), ('Errors', 'Cch'), ('Errors', 'Fld'), ('Errors', 'Thr'), ('Errors', 'ROE'), ('Double Plays', 'Tot'), ('Double Plays', '543'), ('Double Plays', '53'), ('Double Plays', 'GB'), ('Double Plays', 'LD'), ('Double Plays', 'LDs'), ('Double Plays', 'LDf'), ('Unnamed: 30_level_0', 'bFld'), ('Unnamed: 31_level_0', 'bF2O%')]
        self.assertEqual(df_columns, expected_columns)



    def test_player_advanced_fielding_2b(self):

        baseballdc_request = {
            'data_source': 'BASEBALL_REFERENCE',
            'query_params': {
                'scope': 'TEAM',
                'table': 'Player Advanced Fielding -- 2B',
                'year': '2021',
                'team': 'DET'
            }
        }

        df = baseballdc.get_data(baseballdc_request)
        df_columns = list(df.columns.values)

        expected_columns = [('Unnamed: 0_level_0', 'Name'), ('Unnamed: 1_level_0', 'Age'), ('Unnamed: 2_level_0', 'PA'), ('Unnamed: 3_level_0', 'RHB%'), ('Unnamed: 4_level_0', 'BIP%'), ('Unnamed: 5_level_0', 'GBIP%'), ('Unnamed: 6_level_0', 'Fld'), ('Unnamed: 7_level_0', 'F2O%'), ('Unnamed: 8_level_0', 'FC'), ('Putouts', 'Tot'), ('Putouts', 'Cgt'), ('Putouts', 'Frc'), ('Putouts', 'Tag'), ('Assists', 'Tot'), ('Assists', '1B'), ('Assists', '2B'), ('Assists', 'Hm'), ('Assists', 'Rly'), ('Errors', 'Tot'), ('Errors', 'Cch'), ('Errors', 'Fld'), ('Errors', 'Thr'), ('Errors', 'ROE'), ('Double Plays', 'Tot'), ('Double Plays', '543'), ('Double Plays', '53'), ('Double Plays', 'GB'), ('Double Plays', 'LD'), ('Double Plays', 'LDs'), ('Double Plays', 'LDf'), ('Unnamed: 30_level_0', 'bFld'), ('Unnamed: 31_level_0', 'bF2O%')]
        self.assertEqual(df_columns, expected_columns)


    def test_player_advanced_fielding_3b(self):

        baseballdc_request = {
            'data_source': 'BASEBALL_REFERENCE',
            'query_params': {
                'scope': 'TEAM',
                'table': 'Player Advanced Fielding -- 3B',
                'year': '2021',
                'team': 'DET'
            }
        }

        df = baseballdc.get_data(baseballdc_request)
        df_columns = list(df.columns.values)

        expected_columns = [('Unnamed: 0_level_0', 'Name'), ('Unnamed: 1_level_0', 'Age'), ('Unnamed: 2_level_0', 'PA'), ('Unnamed: 3_level_0', 'RHB%'), ('Unnamed: 4_level_0', 'BIP%'), ('Unnamed: 5_level_0', 'GBIP%'), ('Unnamed: 6_level_0', 'Fld'), ('Unnamed: 7_level_0', 'F2O%'), ('Unnamed: 8_level_0', 'FC'), ('Putouts', 'Tot'), ('Putouts', 'Cgt'), ('Putouts', 'Frc'), ('Putouts', 'Tag'), ('Assists', 'Tot'), ('Assists', '1B'), ('Assists', '2B'), ('Assists', 'Hm'), ('Assists', 'Rly'), ('Errors', 'Tot'), ('Errors', 'Cch'), ('Errors', 'Fld'), ('Errors', 'Thr'), ('Errors', 'ROE'), ('Double Plays', 'Tot'), ('Double Plays', '543'), ('Double Plays', '53'), ('Double Plays', 'GB'), ('Double Plays', 'LD'), ('Double Plays', 'LDs'), ('Double Plays', 'LDf'), ('Unnamed: 30_level_0', 'bFld'), ('Unnamed: 31_level_0', 'bF2O%')]
        self.assertEqual(df_columns, expected_columns)


    def test_player_advanced_fielding_ss(self):

        baseballdc_request = {
            'data_source': 'BASEBALL_REFERENCE',
            'query_params': {
                'scope': 'TEAM',
                'table': 'Player Advanced Fielding -- SS',
                'year': '2021',
                'team': 'DET'
            }
        }

        df = baseballdc.get_data(baseballdc_request)
        df_columns = list(df.columns.values)

        expected_columns = [('Unnamed: 0_level_0', 'Name'), ('Unnamed: 1_level_0', 'Age'), ('Unnamed: 2_level_0', 'PA'), ('Unnamed: 3_level_0', 'RHB%'), ('Unnamed: 4_level_0', 'BIP%'), ('Unnamed: 5_level_0', 'GBIP%'), ('Unnamed: 6_level_0', 'Fld'), ('Unnamed: 7_level_0', 'F2O%'), ('Unnamed: 8_level_0', 'FC'), ('Putouts', 'Tot'), ('Putouts', 'Cgt'), ('Putouts', 'Frc'), ('Putouts', 'Tag'), ('Assists', 'Tot'), ('Assists', '1B'), ('Assists', '2B'), ('Assists', 'Hm'), ('Assists', 'Rly'), ('Errors', 'Tot'), ('Errors', 'Cch'), ('Errors', 'Fld'), ('Errors', 'Thr'), ('Errors', 'ROE'), ('Double Plays', 'Tot'), ('Double Plays', '643'), ('Double Plays', '63'), ('Double Plays', '463'), ('Double Plays', '163'), ('Double Plays', '363'), ('Double Plays', 'GB'), ('Double Plays', 'GBs'), ('Double Plays', 'GBr'), ('Double Plays', 'LD'), ('Double Plays', 'LDs'), ('Double Plays', 'LDf')]
        self.assertEqual(df_columns, expected_columns)


    def test_player_advanced_fielding_lf(self):

        baseballdc_request = {
            'data_source': 'BASEBALL_REFERENCE',
            'query_params': {
                'scope': 'TEAM',
                'table': 'Player Advanced Fielding -- LF',
                'year': '2021',
                'team': 'DET'
            }
        }

        df = baseballdc.get_data(baseballdc_request)
        df_columns = list(df.columns.values)

        expected_columns = [('Unnamed: 0_level_0', 'Name'), ('Unnamed: 1_level_0', 'Age'), ('Errors', 'Tot'), ('Errors', 'Cch'), ('Errors', 'Fld'), ('Errors', 'Thr'), ('Errors', 'ROE'), ('Assists', 'Tot'), ('Assists', '1B'), ('Assists', '2B'), ('Assists', '3B'), ('Assists', 'Hm'), ('Single w/ Runner on 1st', 'Opp'), ('Single w/ Runner on 1st', 'Held'), ('Single w/ Runner on 1st', 'Kill'), ('Single w/ Runner on 2nd', 'Opp'), ('Single w/ Runner on 2nd', 'Held'), ('Single w/ Runner on 2nd', 'Kill'), ('Double w/ Runner on 1st', 'Opp'), ('Double w/ Runner on 1st', 'Held'), ('Double w/ Runner on 1st', 'Kill'), ('Flyout, <2out, Runner on 3rd', 'Opp'), ('Flyout, <2out, Runner on 3rd', 'Held'), ('Flyout, <2out, Runner on 3rd', 'Kill'), ('Flyout, <2out, Runner on 2nd', 'Opp'), ('Flyout, <2out, Runner on 2nd', 'Held'), ('Flyout, <2out, Runner on 2nd', 'Kill'), ('Baserunning Totals', 'Opp'), ('Baserunning Totals', 'Held'), ('Baserunning Totals', 'Held%'), ('Baserunning Totals', 'Adv'), ('Baserunning Totals', 'Kill'), ('Baserunning Totals', 'Kill%'), ('Baserunning Totals', 'Aother'), ('Unnamed: 34_level_0', 'PA'), ('Unnamed: 35_level_0', 'RHB%'), ('Unnamed: 36_level_0', 'BIP%'), ('Unnamed: 37_level_0', 'FBIP%'), ('Unnamed: 38_level_0', 'Fld'), ('Unnamed: 39_level_0', 'F2O%')]
        self.assertEqual(df_columns, expected_columns)


    def test_player_advanced_fielding_cf(self):

        baseballdc_request = {
            'data_source': 'BASEBALL_REFERENCE',
            'query_params': {
                'scope': 'TEAM',
                'table': 'Player Advanced Fielding -- CF',
                'year': '2021',
                'team': 'DET'
            }
        }

        df = baseballdc.get_data(baseballdc_request)
        df_columns = list(df.columns.values)

        expected_columns = [('Unnamed: 0_level_0', 'Name'), ('Unnamed: 1_level_0', 'Age'), ('Errors', 'Tot'), ('Errors', 'Cch'), ('Errors', 'Fld'), ('Errors', 'Thr'), ('Errors', 'ROE'), ('Assists', 'Tot'), ('Assists', '1B'), ('Assists', '2B'), ('Assists', '3B'), ('Assists', 'Hm'), ('Single w/ Runner on 1st', 'Opp'), ('Single w/ Runner on 1st', 'Held'), ('Single w/ Runner on 1st', 'Kill'), ('Single w/ Runner on 2nd', 'Opp'), ('Single w/ Runner on 2nd', 'Held'), ('Single w/ Runner on 2nd', 'Kill'), ('Double w/ Runner on 1st', 'Opp'), ('Double w/ Runner on 1st', 'Held'), ('Double w/ Runner on 1st', 'Kill'), ('Flyout, <2out, Runner on 3rd', 'Opp'), ('Flyout, <2out, Runner on 3rd', 'Held'), ('Flyout, <2out, Runner on 3rd', 'Kill'), ('Flyout, <2out, Runner on 2nd', 'Opp'), ('Flyout, <2out, Runner on 2nd', 'Held'), ('Flyout, <2out, Runner on 2nd', 'Kill'), ('Baserunning Totals', 'Opp'), ('Baserunning Totals', 'Held'), ('Baserunning Totals', 'Held%'), ('Baserunning Totals', 'Adv'), ('Baserunning Totals', 'Kill'), ('Baserunning Totals', 'Kill%'), ('Baserunning Totals', 'Aother'), ('Unnamed: 34_level_0', 'PA'), ('Unnamed: 35_level_0', 'RHB%'), ('Unnamed: 36_level_0', 'BIP%'), ('Unnamed: 37_level_0', 'FBIP%'), ('Unnamed: 38_level_0', 'Fld'), ('Unnamed: 39_level_0', 'F2O%')]
        self.assertEqual(df_columns, expected_columns)


    def test_player_advanced_fielding_rf(self):

        baseballdc_request = {
            'data_source': 'BASEBALL_REFERENCE',
            'query_params': {
                'scope': 'TEAM',
                'table': 'Player Advanced Fielding -- RF',
                'year': '2021',
                'team': 'DET'
            }
        }

        df = baseballdc.get_data(baseballdc_request)
        df_columns = list(df.columns.values)

        expected_columns = [('Unnamed: 0_level_0', 'Name'), ('Unnamed: 1_level_0', 'Age'), ('Errors', 'Tot'), ('Errors', 'Cch'), ('Errors', 'Fld'), ('Errors', 'Thr'), ('Errors', 'ROE'), ('Assists', 'Tot'), ('Assists', '1B'), ('Assists', '2B'), ('Assists', '3B'), ('Assists', 'Hm'), ('Single w/ Runner on 1st', 'Opp'), ('Single w/ Runner on 1st', 'Held'), ('Single w/ Runner on 1st', 'Kill'), ('Single w/ Runner on 2nd', 'Opp'), ('Single w/ Runner on 2nd', 'Held'), ('Single w/ Runner on 2nd', 'Kill'), ('Double w/ Runner on 1st', 'Opp'), ('Double w/ Runner on 1st', 'Held'), ('Double w/ Runner on 1st', 'Kill'), ('Flyout, <2out, Runner on 3rd', 'Opp'), ('Flyout, <2out, Runner on 3rd', 'Held'), ('Flyout, <2out, Runner on 3rd', 'Kill'), ('Flyout, <2out, Runner on 2nd', 'Opp'), ('Flyout, <2out, Runner on 2nd', 'Held'), ('Flyout, <2out, Runner on 2nd', 'Kill'), ('Baserunning Totals', 'Opp'), ('Baserunning Totals', 'Held'), ('Baserunning Totals', 'Held%'), ('Baserunning Totals', 'Adv'), ('Baserunning Totals', 'Kill'), ('Baserunning Totals', 'Kill%'), ('Baserunning Totals', 'Aother'), ('Unnamed: 34_level_0', 'PA'), ('Unnamed: 35_level_0', 'RHB%'), ('Unnamed: 36_level_0', 'BIP%'), ('Unnamed: 37_level_0', 'FBIP%'), ('Unnamed: 38_level_0', 'Fld'), ('Unnamed: 39_level_0', 'F2O%')]
        self.assertEqual(df_columns, expected_columns)



    def test_player_advanced_fielding_p(self):

        baseballdc_request = {
            'data_source': 'BASEBALL_REFERENCE',
            'query_params': {
                'scope': 'TEAM',
                'table': 'Player Advanced Fielding -- P',
                'year': '2021',
                'team': 'DET'
            }
        }

        df = baseballdc.get_data(baseballdc_request)
        df_columns = list(df.columns.values)

        expected_columns = [('Unnamed: 0_level_0', 'Name'), ('Unnamed: 1_level_0', 'Age'), ('Unnamed: 2_level_0', 'PA'), ('Unnamed: 3_level_0', 'BIP%'), ('Unnamed: 4_level_0', 'GBIP%'), ('Unnamed: 5_level_0', 'Fld'), ('Unnamed: 6_level_0', 'F2O%'), ('Unnamed: 7_level_0', 'FC'), ('Putouts', 'Tot'), ('Putouts', 'Cgt'), ('Putouts', '31'), ('Assists', 'Tot'), ('Assists', '1B'), ('Assists', '2B'), ('Errors', 'Tot'), ('Errors', 'Cch'), ('Errors', 'Fld'), ('Errors', 'Thr'), ('Errors', 'ROE'), ('Double Plays', 'Tot'), ('Double Plays', '163'), ('Double Plays', 'GB'), ('Double Plays', 'LD'), ('Unnamed: 23_level_0', 'bFld'), ('Unnamed: 24_level_0', 'bF2O%')]
        self.assertEqual(df_columns, expected_columns)




    def test_year_by_year_team_batting(self):

        baseballdc_request = {
            'data_source': 'BASEBALL_REFERENCE',
            'query_params': {
                'scope': 'TEAM',
                'table': 'Year-by-Year Team Batting',
                'year': '2021',
                'team': 'DET'
            }
        }

        df = baseballdc.get_data(baseballdc_request)
        df_columns = list(df.columns.values)

        expected_columns = ['Year', 'Lg', 'W', 'L', 'Finish', 'R/G', 'G', 'PA', 'AB', 'R', 'H', '2B', '3B', 'HR', 'RBI', 'SB', 'CS', 'BB', 'SO', 'BA', 'OBP', 'SLG', 'OPS', 'E', 'DP', 'Fld%', 'BatAge']
        self.assertEqual(df_columns, expected_columns)



    def test_year_by_year_team_batting_per_game(self):

        baseballdc_request = {
            'data_source': 'BASEBALL_REFERENCE',
            'query_params': {
                'scope': 'TEAM',
                'table': 'Year-by-Year Team Batting per Game',
                'year': '2021',
                'team': 'DET'
            }
        }

        df = baseballdc.get_data(baseballdc_request)
        df_columns = list(df.columns.values)

        expected_columns = ['Year', 'Lg', 'W', 'L', 'Finish', 'G', 'PA', 'AB', 'R', 'H', '2B', '3B', 'HR', 'RBI', 'SB', 'CS', 'BB', 'SO', 'BA', 'OBP', 'SLG', 'OPS', 'E', 'DP', 'Fld%']
        self.assertEqual(df_columns, expected_columns)


    def test_year_by_year_team_batting_ranks(self):

        baseballdc_request = {
            'data_source': 'BASEBALL_REFERENCE',
            'query_params': {
                'scope': 'TEAM',
                'table': 'Year-by-Year Team Batting Ranks',
                'year': '2021',
                'team': 'DET'
            }
        }

        df = baseballdc.get_data(baseballdc_request)
        df_columns = list(df.columns.values)

        expected_columns = ['Year', 'Lg', 'W', 'L', 'Finish', 'R/G', 'G', 'AB', 'R', 'H', '2B', '3B', 'HR', 'SB', 'CS', 'BB', 'SO', 'BA', 'OBP', 'SLG', 'OPS', 'E', 'DP', 'Fld%', 'BatAge']
        self.assertEqual(df_columns, expected_columns)




    def test_year_by_year_team_pitching(self):

        baseballdc_request = {
            'data_source': 'BASEBALL_REFERENCE',
            'query_params': {
                'scope': 'TEAM',
                'table': 'Year-by-Year Team Pitching',
                'year': '2021',
                'team': 'DET'
            }
        }

        df = baseballdc.get_data(baseballdc_request)
        df_columns = list(df.columns.values)

        expected_columns = ['Year', 'Lg', 'W', 'L', 'Finish', 'RA/G', 'ERA', 'G', 'CG', 'tSho', 'SV', 'IP', 'H', 'R', 'ER', 'HR', 'BB', 'SO', 'WHIP', 'SO9', 'HR9', 'E', 'DP', 'Fld%', 'PAge']
        self.assertEqual(df_columns, expected_columns)


    def test_year_by_year_team_pitching_per_game(self):

        baseballdc_request = {
            'data_source': 'BASEBALL_REFERENCE',
            'query_params': {
                'scope': 'TEAM',
                'table': 'Year-by-Year Team Pitching per Game',
                'year': '2021',
                'team': 'DET'
            }
        }

        df = baseballdc.get_data(baseballdc_request)
        df_columns = list(df.columns.values)

        expected_columns = ['Year', 'Lg', 'W', 'L', 'Finish', 'RA/G', 'ERA', 'G', 'CG', 'tSho', 'SV', 'IP', 'H', 'R', 'ER', 'HR', 'BB', 'SO', 'WHIP', 'SO9', 'HR9', 'E', 'DP', 'Fld%', 'PAge']
        self.assertEqual(df_columns, expected_columns)


    def test_year_by_year_team_pitching_ranks(self):

        baseballdc_request = {
            'data_source': 'BASEBALL_REFERENCE',
            'query_params': {
                'scope': 'TEAM',
                'table': 'Year-by-Year Team Pitching Ranks',
                'year': '2021',
                'team': 'DET'
            }
        }

        df = baseballdc.get_data(baseballdc_request)
        df_columns = list(df.columns.values)

        expected_columns = ['Year', 'Lg', 'W', 'L', 'Finish', 'RA/G', 'ERA', 'G', 'CG', 'tSho', 'SV', 'IP', 'H', 'R', 'ER', 'HR', 'BB', 'SO', 'WHIP', 'SO9', 'HR9', 'E', 'DP', 'Fld%', 'PAge']
        self.assertEqual(df_columns, expected_columns)

if __name__ == '__main__':
        unittest.main()

