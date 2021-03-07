"""
Fetch Core Web Vitals from the Google PageSpeed Insights API.
"""

import sys
import json
import urllib.request
import pandas as pd


def query_core_web_vitals(key: str,
                          url: str,
                          strategy: str = "desktop"):
    """Run a Google Page Speed API query to fetch the Core Web Vitals for a URL.

    Args:
        key (str): API key for Google Page Speed API.
        url (str): URL of the page you wish to check.
        strategy (str, optional): Optional strategy (desktop or mobile).

    Returns:
        data (json): API response in JSON format.
    """

    try:
        endpoint = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed" \
                   + "?strategy=" + strategy \
                   + "&url={}" \
                   + "&key=" + key

        response = urllib.request.urlopen(endpoint.format(url)).read().decode('UTF-8')
        data = json.loads(response)
        return data
    except Exception as e:
        print("Error: ", e)
        sys.exit(1)


def save_core_web_vitals(report: dict,
                         filename: str):
    """Save the Core Web Vitals JSON report to file.

    Args:
        report (dict): JSON object containing report data.
        filename (str): Filename to use for report.

    Returns:
        JSON Core Web Vitals report file.
    """

    with open(filename, 'w') as outfile:
        json.dump(report, outfile)


def parse_core_web_vitals(report: dict):
    """Return a dictionary containing the Core Web Vitals from the report.

    Args:
        report (dict): JSON dictionary containing report data.

    Return:
        data (dict): Dictionary containing the key data.

    """

    final_url = report['lighthouseResult']['finalUrl']
    fetch_time = report['lighthouseResult']['fetchTime']
    form_factor = report['lighthouseResult']['configSettings']['formFactor']
    overall_score = report["lighthouseResult"]["categories"]["performance"]["score"] * 100
    speed_index = report["lighthouseResult"]["audits"]["speed-index"]["score"] * 100
    first_meaningful_paint = report["lighthouseResult"]["audits"]["first-meaningful-paint"]["score"] * 100
    first_contentful_paint = report["lighthouseResult"]["audits"]["first-contentful-paint"]["score"] * 100
    time_to_interactive = report["lighthouseResult"]["audits"]["interactive"]["score"] * 100
    total_blocking_time = report["lighthouseResult"]["audits"]["total-blocking-time"]["score"] * 100
    cumulative_layout_shift = report["lighthouseResult"]["audits"]["cumulative-layout-shift"]["score"] * 100

    data = {
        'final_url': final_url,
        'fetch_time': fetch_time,
        'form_factor': form_factor,
        'overall_score': overall_score,
        'speed_index': speed_index,
        'first_meaningful_paint': first_meaningful_paint,
        'first_contentful_paint': first_contentful_paint,
        'time_to_interactive': time_to_interactive,
        'total_blocking_time': total_blocking_time,
        'cumulative_layout_shift': cumulative_layout_shift,
    }

    return data


def get_core_web_vitals(key: str,
                        urls: list,
                        strategy: str = "both"):
    """Return a Pandas dataframe containing Core Web Vitals for the provided URLs and optional strategy.

    Args:
        key (str): API key for Google Page Speed API.
        urls (list): URL of the page you wish to check.
        strategy (str, optional): Optional strategy (desktop or mobile) or both (default).

    Returns:
        df (dataframe): Pandas dataframe containing core web vitals for URL and strategy.
    """

    df = pd.DataFrame(columns=['final_url', 'fetch_time', 'form_factor', 'overall_score',
                               'speed_index', 'first_meaningful_paint', 'first_contentful_paint',
                               'time_to_interactive', 'total_blocking_time', 'cumulative_layout_shift'])

    if strategy == "both":

        for url in urls:
            report = query_core_web_vitals(key, url, strategy="mobile")
            if report:
                data = parse_core_web_vitals(report)
                df = df.append(data, ignore_index=True)

        for url in urls:
            report = query_core_web_vitals(key, url, strategy="desktop")
            if report:
                data = parse_core_web_vitals(report)
                df = df.append(data, ignore_index=True)

    else:
        for url in urls:
            report = query_core_web_vitals(key, url, strategy=strategy)
            if report:
                data = parse_core_web_vitals(report)
                df = df.append(data, ignore_index=True)

    df = df.sort_values(by='final_url')
    return df
