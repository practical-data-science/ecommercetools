"""
Fetch data from the Google Search Console API.
"""

import sys
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build


def _connect(key: str):
    """Create a connection to the Google Search Console API and return service object.

    Args:
        key (string): Google Search Console JSON client secrets path.

    Returns:
        service (object): Google Search Console service object.
    """

    try:
        scope = ['https://www.googleapis.com/auth/webmasters']
        credentials = service_account.Credentials.from_service_account_file(key, scopes=scope)
        service = build('webmasters', 'v3', credentials=credentials)

        return service

    except Exception as e:
        print("Error: ", e)
        sys.exit(1)


def _get_response(service, site_url, payload):
    """Returns the rowLimit value from a Google Search Console API payload.

    Args:
        service (object): Google Search Console service object.
        site_url (string): Site URL for the Google Search Console property.
                           For domain properties use "sc-domain:example.com".
                           For other properties use "https://www.example.com".
        payload (dict): Google Search Console API payload.

    Returns:
        response (dict): API response dictionary
    """

    try:
        return service.searchanalytics().query(siteUrl=site_url, body=payload).execute()
    except Exception as e:
        return e


def _get_results(service, site_url, payload, results):
    """Returns a dictionary containing the Google Search Console API query results.

    Args:
        service (object): Google Search Console service object.
        site_url (string): Site URL for the Google Search Console property.
                           For domain properties use "sc-domain:example.com".
                           For other properties use "https://www.example.com".
        payload (dict): Google Search Console API payload.
        results (list): Python list to which to append the results.

    Returns:
        results (dict): Python dictionary of results to use to create a dataframe.

    """

    response = _get_response(service, site_url, payload)

    try:
        for row in response['rows']:
            data = {}

            for i in range(len(payload['dimensions'])):
                data[payload['dimensions'][i]] = row['keys'][i]

            data['clicks'] = row['clicks']
            data['impressions'] = row['impressions']
            data['ctr'] = round(row['ctr'] * 100, 2)
            data['position'] = round(row['position'], 2)
            results.append(data)

        return results
    except Exception as e:
        return None


def query_google_search_console(key: str, site_url: str, payload: dict, fetch_all=False):
    """Run a query on the Google Search Console API and return a dataframe of results.

    Args:
        key (object): JSON client secrets key file path.
        site_url (string): URL of Google Search Console property
        payload (dict): API query payload dictionary
        fetch_all (boolean, default=False): Set to True to return all results and ignore rowLimit and startRow if provided

    Return:
        df (dataframe): Pandas dataframe containing requested data.
    """

    service = _connect(key)
    results = []

    if fetch_all == False:
        results = _get_results(service, site_url, payload, results)
    else:
        maxrows = 10000
        startrow = 0
        complete = False

        while not complete:
            payload['rowLimit'] = maxrows
            payload['startRow'] = startrow
            result = _get_results(service, site_url, payload, results)

            if result is None:
                complete = True

            startrow += maxrows
    return pd.DataFrame.from_dict(results)


def query_google_search_console_compare(key, site_url, payload_before, payload_after, fetch_all=False):
    """Run two queries on the Google Search Console API and return a dataframe of results comparing changes.

    Args:
        key (object): JSON client secrets key file path.
        site_url (string): URL of Google Search Console property
        payload_before (dict): API query payload dictionary for earliest period
        payload_after (dict): API query payload dictionary for latest period
        fetch_all (boolean, default=False): Set to True to return all results and ignore rowLimit and startRow if provided

    Example:

    The below code will compare queries by page and device across two periods and return a dataframe of results.

    payload_before = {
    'startDate': "2021-08-11",
    'endDate': "2021-08-31",
    'dimensions': ["page","query", "device"],
    }

    payload_after = {
        'startDate': "2021-07-21",
        'endDate': "2021-08-10",
        'dimensions': ["page","query", "device"],
    }

    df = query_google_search_console_compare(key, site_url, payload_before, payload_after, fetch_all=False)

    Return:
        df (dataframe): Pandas dataframe containing requested data.
    """

    # Validate the payload
    if ('date' in payload_before['dimensions']) or ('date' in payload_after['dimensions']):
        print('The date dimension cannot be used in a payload. Please use only page, query, and device.')
    elif payload_before['dimensions'] != payload_after['dimensions']:
        print('The payload dimensions provided do not match. Please use the same dimensions in each payload.')
    else:
        # Fetch the data and prefix the column names with _before and _after
        df_before = query_google_search_console(key, site_url, payload_before, fetch_all=fetch_all)
        df_after = query_google_search_console(key, site_url, payload_after, fetch_all=fetch_all)
        df_before.columns = [str(col) + '_before' for col in df_before.columns]
        df_after.columns = [str(col) + '_after' for col in df_after.columns]

        # Extract the dimensions from the payload, remove date and append _before and _after and join data
        dimensions_before = [dimension + '_before' for dimension in payload_before['dimensions']]
        dimensions_after = [dimension + '_after' for dimension in payload_after['dimensions']]
        df = df_before.merge(df_after, how='left', left_on=dimensions_before, right_on=dimensions_after)
        df = df.fillna(0)

        # Calculate changes between the periods
        df['clicks_change'] = df['clicks_after'] - df['clicks_before']
        df['impressions_change'] = df['impressions_after'] - df['impressions_before']
        df['ctr_change'] = df['ctr_after'] - df['ctr_before']
        df['position_change'] = df['position_after'] - df['position_before']

        # Drop the _after suffixed columns from the dataframe
        object_columns = list(df.select_dtypes(['object']).columns)
        after_columns = [column for column in object_columns if "_after" in column]
        df = df.drop(columns=after_columns)

        # Create the dataframe
        dimension_columns = list(df.select_dtypes(['object']).columns)
        metrics = ['impressions_before',
                   'impressions_after',
                   'impressions_change',
                    'clicks_before',
                   'clicks_after',
                   'clicks_change',
                   'ctr_before',
                   'ctr_after',
                   'ctr_change',
                   'position_before',
                   'position_after',
                   'position_change']
        df = df[dimension_columns + metrics]

        # Drop the _before from dimension columns
        df.columns = df.columns.str.replace('page_before', 'page')
        df.columns = df.columns.str.replace('query_before', 'query')
        df.columns = df.columns.str.replace('device_before', 'device')

        return df
