# baseballdc
## Baseball Data Center (v1.0.0)

Baseball Data Center was created with the goal of making the data retrieval process for baseball statistics simple.

The baseballdc library exposes one function to the end user, the `get_data` function. By calling this function with the required parameter object, you can retrieve baseball statistics in a Pandas DataFrame to use in your Python project.

## How to install baseballdc:

Use pip to install baseballdc:

```bash
pip install baseballdc
```

## How to use baseballdc:


To retrieve data with baseballdc, you need to pass a Python dictionary as a parameter into the `get_data` function. (If you are not familiar with Python dictionaries, [here](https://www.w3schools.com/python/python_dictionaries.asp) is a quick overview.)


The format of the dictionary that the `get_data` function requires is: 

```python
{
	'data_source': string,
	'query_params': {
		'scope': string,
		'table': string
	}
}
```

## How to Configure the Request Parameter:

baseballdc currently only scrapes data from Baseball Reference, so the `data_source` should be set to `'BASEBALL_REFERENCE'`.

```python
'data_source': 'BASEBALL_REFERENCE',
```

The `query_param` object is itself a dictionary, with two required values, and multiple optional values.

The two required values are `scope`, and `table`.

The `scope` of the data you can retrieve is one of three options: 

* 'INDIVIDUAL_PLAYER'
* 'TEAM'
* 'SEASON'

The `table` is the name of the table on Baseball Reference

For example the request: 

```python
{
        'data_source': 'BASEBALL_REFERENCE',
        'query_params': {
                'scope': 'TEAM',
                'table': 'Active Franchises',
        }
}
```

will retrieve the Active Franchises table, that can be found [here](https://www.baseball-reference.com/teams/) on Baseball Reference. 

There are also optional values that can be included in `query_params`. These are used to further specify which table you are requesting. The list of accepted optional parameters are

* first_name
* last_name
* team
* league
* year


## Examples
A few example requests you could make are below.

Retrieve Shohei Ohtani's Player Value--Pitching table, found [here](https://www.baseball-reference.com/players/o/ohtansh01.shtml#pitching_value) on Baseball Reference:

```python
{
        'data_source': 'BASEBALL_REFERENCE',
        'query_params': {
                'scope': 'INDIVIDUAL_PLAYER',
                'table': 'Player Value--Pitching',
                'first_name': 'Shohei',
                'last_name': 'Ohtani'
        }
}
```

Retrieve Juan Soto's Advanced Batting table, found [here](https://www.baseball-reference.com/players/s/sotoju01.shtml#batting_advanced) on Baseball Reference:

```python
{
        'data_source': 'BASEBALL_REFERENCE',
        'query_params': {
                'scope': 'INDIVIDUAL_PLAYER',
                'table': 'Advanced Batting',
                'first_name': 'Juan',
                'last_name': 'Soto'
        }
}
```

Retrieve the Detroit Tigers 2021 Team Pitching table, found [here](https://www.baseball-reference.com/teams/DET/2021.shtml#team_pitching) on Baseball Reference:

```python
{
        'data_source': 'BASEBALL_REFERENCE',
        'query_params': {
                'scope': 'TEAM',
                'table': 'Team Pitching',
                'team': 'DET',
                'year': '2021'
        }
}
```

Retrieve the National League's Team Standard Batting table for the 2021 season, found [here](https://www.baseball-reference.com/leagues/NL/2021.shtml#teams_standard_batting) on Baseball Reference:
```python
{
            'data_source': 'BASEBALL_REFERENCE',
            'query_params': {
                'scope': 'SEASON',
                'table': 'Team Standard Batting',
                'league': 'NL',
                'year': '2021'
            }
        }
```


## Putting It All Together

```python
import baseballdc

baseballdc_request = {
	'data_source': 'BASEBALL_REFERENCE',
	'query_params': {
                'scope': 'INDIVIDUAL_PLAYER',
                'table': 'Standard Batting',
                'first_name': 'Shohei',
                'last_name': 'Ohtani'
	}
}

data_frame = baseballdc.get_data(baseballdc_request)
```