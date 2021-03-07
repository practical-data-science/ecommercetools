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


def query_google_search_console(key: str, site_url: str, payload: dict):
    """Run a query on the Google Search Console API and return a dataframe of results.

    Args:
        key (object): JSON client secrets key file path.
        site_url (string): URL of Google Search Console property
        payload (dict): API query payload dictionary

    Return:
        df (dataframe): Pandas dataframe containing requested data.
    """

    service = _connect(key)

    response = service.searchanalytics().query(siteUrl=site_url, body=payload).execute()

    results = []

    for row in response['rows']:
        data = {}

        for i in range(len(payload['dimensions'])):
            data[payload['dimensions'][i]] = row['keys'][i]

        data['clicks'] = row['clicks']
        data['impressions'] = row['impressions']
        data['ctr'] = round(row['ctr'] * 100, 2)
        data['position'] = round(row['position'], 2)
        results.append(data)

    return pd.DataFrame.from_dict(results)


