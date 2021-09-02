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
