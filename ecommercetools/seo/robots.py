"""
Fetch the contents of a robots.txt file and return the output in a Pandas dataframe.
"""

import requests
import urllib.parse
import json
import pandas as pd
from requests_html import HTMLSession


def _get_source(url: str):
    """Return the source code for the provided URL.

    Args:
        url (string): URL of the page to scrape.

    Returns:
        response (object): HTTP response object from requests_html.
    """

    try:
        session = HTMLSession()
        response = session.get(url)
        return response
    except requests.exceptions.RequestException as e:
        print(e)


def get_sitemaps(url: str):
    """Parse a robots.txt file and return a Python list containing any sitemap URLs found.

    Args:
        url (string): URL of robots.txt file.

    Returns:
        data (list): List containing each sitemap found.
    """

    response = _get_source(url)
    robots = response.text

    data = []
    lines = str(robots).splitlines()

    for line in lines:
        if line.startswith('Sitemap:'):
            split = line.split(':', maxsplit=1)
            data.append(split[1].strip())

    return data


def get_robots(url: str):
    """Parses robots.txt file contents into a Pandas DataFrame.

    Args:
        url (string): URL of robots.txt file.

    Returns:
        df (list): Pandas dataframe containing robots.txt directives and parameters.
    """

    response = _get_source(url)
    robots = response.text

    data = []
    lines = str(robots).splitlines()
    for line in lines:

        if line.strip():
            if not line.startswith('#'):
                split = line.split(':', maxsplit=1)
                data.append([split[0].strip(), split[1].strip()])

    return pd.DataFrame(data, columns=['directive', 'parameter'])

