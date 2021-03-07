"""
General functions for scraping data from Google search engine results pages.
"""

import requests
import urllib.parse
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


def _get_site_results(url: str):
    """Return the source of a site:url search.

    Args:
        url: URL of page to append to site: query

    Returns:
        response (str): HTML of page.
    """

    query = urllib.parse.quote_plus(url)
    response = _get_source("https://www.google.co.uk/search?q=site%3A" + query)

    return response


def _parse_site_results(response: str):
    """Parse the HTML of a site:url query and return the number of pages "indexed".

    Args:
        response: HTML of site:url query.

    Returns:
        indexed: Number of pages "indexed".
    """

    string = response.html.find("#result-stats", first=True).text
    indexed = int(string.split(' ')[1].replace(',', ''))
    return indexed


def _count_indexed_pages(url: str):
    """Gets the site:url data, parses the response, and returns the number of "indexed" pages.

    Args:
        url: URL to use in site:url search.

    Returns:
        results (int): Number of pages "indexed".
    """

    response = _get_site_results(url)
    return _parse_site_results(response)


def get_indexed_pages(urls: list):
    """Loop through a series of URLs and run site:url searches, then return number of "indexed" pages.

    Args:
        urls (list): List of URLs.

    Returns:
        df (dataframe): Pandas dataframe containing URL and number of "indexed" pages.
    """

    data = []
    for site in urls:
        site_data = {'url': site, 'indexed_pages': _count_indexed_pages(site)}
        data.append(site_data)
    df = pd.DataFrame.from_records(data)
    df = df.sort_values(by='indexed_pages')
    return df


def _get_results(query: str):
    """Return the source of a search.

    Args:
        query: Search query term.

    Returns:
        response (str): HTML of page.
    """

    query = urllib.parse.quote_plus(query)
    response = _get_source("https://www.google.co.uk/search?q=" + query)

    return response


def _parse_search_results(response):
    css_identifier_result = ".tF2Cxc"
    css_identifier_title = "h3"
    css_identifier_link = ".yuRUbf a"
    css_identifier_text = ".IsZvec"

    results = response.html.find(css_identifier_result)

    output = []

    for result in results:
        item = {
            'title': result.find(css_identifier_title, first=True).text,
            'link': result.find(css_identifier_link, first=True).attrs['href'],
            'text': result.find(css_identifier_text, first=True).text
        }

        output.append(item)

    return output


def get_serps(query: str, output="dataframe"):
    """Return the first 10 Google search results for a given query.

    Args:
        query (string): Query term to search Google for.
        output (string): Optional output format (dataframe or dictionary).

    Returns:
        results (dict): Results of query.
    """

    response = _get_results(query)
    results = _parse_search_results(response)

    if results:
        if output == "dataframe":
            df = pd.DataFrame.from_records(results)
            return df
        else:
            return results

