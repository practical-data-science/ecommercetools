"""
General functions for scraping data from Google search engine results pages.
"""

import re
import requests
import urllib.parse
import pandas as pd
import numpy as np
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

        if response.status_code == 200:
            return response
        elif response.status_code == 429:
            print('Error: Too many requests. Google has temporarily blocked you. Try again later.')
            exit()
        else:
            print('Error:' + response)
            exit()
    except requests.exceptions.RequestException as e:
        print(e)


def _get_site_results(url: str):
    """Return the source of a site:url search.

    Args:
        url: URL of page to append to site: query

    Returns:
        response (str): HTML of page.
    """

    try:
        query = urllib.parse.quote_plus(url)
        response = _get_source("https://www.google.co.uk/search?q=site%3A" + query + "&num=100")

        return response
    except requests.exceptions.RequestException as e:
        print(e)


def _parse_site_results(response: str):
    """Parse the HTML of a site:url query and return the number of pages "indexed".

    Args:
        response: HTML of site:url query.

    Returns:
        indexed: Number of pages "indexed".
    """

    try:
        if response.html.find("#result-stats", first=True):

            string = response.html.find("#result-stats", first=True).text
            if string:
                # Remove values in paretheses, i.e. (0.31 seconds)
                string = re.sub(r'\([^)]*\)', '', string)

                # Remove non-numeric characters
                string = re.sub('[^0-9]', '', string)

                return string
            else:
                return 0
    except requests.exceptions.RequestException as e:
        print(e)


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
    response = _get_source("https://www.google.co.uk/search?q=" + query + "&num=100")

    return response


def _get_next_page(response, domain="google.co.uk"):
    """Get the URL for the next page of results."""

    css_identifier_next = "#pnnext"
    next_page_url = response.html.find(css_identifier_next, first=True).attrs['href']
    next_page = "https://www." + domain + next_page_url

    return next_page


def _parse_search_results(response):
    """Parses the Google Search engine results and returns a list of results.

    Note: This function is obviously dependent upon the source code in the Google results.
    Google obfuscates the source of the page to make it more difficult to extra information.
    Extraction classes change from time to time, so there is always a likelihood that this
    function will need to be adjusted with the new class or identifier details.
    In the event of the function failing, please raise a GitHub issue.

    Args:
        response: Response object containing the page source code.

    Returns:
        list: List of Google search results.
    """

    css_identifier_result = ".tF2Cxc"  # The class of the div containing each result, i.e. <div class="tF2Cxc">
    css_identifier_title = "h3"  # The element containing the title, i.e. <h3 class="...
    css_identifier_link = ".yuRUbf a"  # The class of the div containing the anchor, i.e. <div class="yuRUbf"><a ...
    css_identifier_text = ".VwiC3b"  # The class of the parent element containing the snippet <span>
    css_identifier_bold = ".VwiC3b span em"  # The class of the element containing the snippet <span><em>

    try:
        results = response.html.find(css_identifier_result)

        output = []

        for result in results:

            if result.find(css_identifier_text, first=True):
                text = result.find(css_identifier_text, first=True).text
            else:
                text = ''

            if result.find(css_identifier_title, first=True):
                title = result.find(css_identifier_title, first=True).text
            else:
                title = ''

            if result.find(css_identifier_link, first=True):
                link = result.find(css_identifier_link, first=True).attrs['href']
            else:
                link = ''

            # Extract bold text
            if result.find(css_identifier_bold, first=True):
                bold = result.find(css_identifier_bold, first=True).text.lower()
            else:
                bold = ''

            item = {
                'title': title,
                'link': link,
                'text': text,
                'bold': bold,
            }

            output.append(item)

        return output
    except requests.exceptions.RequestException as e:
        print(e)


def get_serps(query: str,
              output="dataframe",
              pages=1,
              domain="google.co.uk"):
    """Return the Google search results for a given query.

    Args:
        query (string): Query term to search Google for.
        output (string, optional): Optional output format (dataframe or dictionary).
        pages (int, optional): Optional number of pages to return.
        domain (string, optional): Optional Google domain (default is google.co.uk).

    Returns:
        results (dict): Results of query.
    """

    response = _get_results(query)
    results = _parse_search_results(response)
    next_page = _get_next_page(response)

    page = 1
    while page <= pages:
        if page > 1:
            response = _get_source(next_page)
            results = results + _parse_search_results(response)
            next_page = _get_next_page(response)
        page += 1

    if results:
        if output == "dataframe":
            df = pd.DataFrame.from_records(results)
            df.index = np.arange(1, len(df) + 1)
            df.index.names = ['position']
            return df.reset_index()
        else:
            return results
