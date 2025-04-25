import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin
import re

def normalize_url(url: str, base_url: str) -> str:
    """
    Normalizes a URL by combining a base URL with a relative URL.

    This function takes a relative URL and a base URL, then combines them into an absolute URL using 
    `urljoin` from the `urllib.parse` module. It ensures that the final URL is properly formatted and 
    handles edge cases such as trailing slashes or incomplete URLs. The resulting URL will have no trailing 
    slash to maintain consistency.

    Args:
        url (str): The relative or absolute URL to normalize. This can be a full URL or a path that needs
                   to be joined with the base URL.
        base_url (str): The base URL used to resolve the relative URL. This is typically the URL of the 
                        current page or site.

    Returns:
        str: The normalized absolute URL, combining the base URL and the provided URL.
    """
    return urljoin(base_url.rstrip('/'), url).rstrip('/')

def get_html(url: str) -> Dict[str, Any]:
    """
    Fetches the HTML content of a given URL with improved error handling and timeout.

    This function makes an HTTP GET request to the specified URL and attempts to retrieve the HTML content. 
    It handles exceptions that may occur during the request (e.g., network errors, invalid URLs, or timeouts) 
    and ensures that the function does not crash. In case of an error, the function returns an error message 
    with the exception type. If the request is successful, the HTML content is returned.

    Args:
        url (str): The URL from which to fetch the HTML content. It should be a valid, accessible URL.

    Returns:
        Dict[str, Any]: A dictionary containing:
            - 'url' (str): The URL that was requested.
            - 'error' (str or None): The type of error (if any), or None if the request was successful.
            - 'html' (str or None): The HTML content of the page, or None if the request failed.

    """
    response = {'url': url, 'error': None, 'html': None}
    try:
        with requests.get(url, timeout=10) as res:
            res.raise_for_status()
            response['html'] = res.text
    except requests.RequestException as e:
        response['error'] = type(e).__name__
    return response

def parse_html(base_url: str, html: str) -> List[Dict[str, Any]]:
    """
    Parses the HTML content to extract service names and corresponding links.

    This function takes the HTML content of a page and searches for specific sections 
    related to services. It looks for a div with a specific ID and searches for links
    containing certain keywords. The function returns a list of dictionaries where each
    dictionary contains the name of the service and its associated link.

    Args:
        base_url (str): The base URL used to normalize relative URLs in the HTML content.
        html (str): The raw HTML content of the page to parse.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries, each containing:
            - 'service_name' (str): The name of the service (text inside the anchor tag).
            - 'link_of_service' (str): The absolute URL of the service (normalized from the href attribute).

    """
    if not html:
        return []
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # Combined search for services div using a list of selectors
    selectors = [
        lambda s: s.find('div', id='block-menu-menu-egov-services'),
        lambda s: s.find('a', text=re.compile('विधुतीय|विद्युतीय', re.IGNORECASE))
    ]
    
    services_div = None
    for selector in selectors:
        services_div = selector(soup)
        if services_div:
            break
    
    if not services_div:
        return []
    
    if services_div.name == 'a':
        services_div = services_div.find_parent('li')
    
    return [
        {
            'service_name': link.get_text(strip=True),
            'link_of_service': normalize_url(link['href'].strip(), base_url)
        }
        for link in services_div.find_all('a', href=True)
        if link.get_text(strip=True) and link['href'].strip()
    ]

def process_url(url: str) -> Dict[str, Any]:
    """
    Processes a single URL to extract data from its HTML content.

    This function retrieves the HTML content from the specified URL and processes it to extract relevant data.
    It uses the `get_html` function to fetch the page, and if successful, it parses the content using the
    `parse_html` function. The result is returned as a dictionary, where the key is the URL, and the value is
    either an error message or the parsed data from the HTML.

    Args:
        url (str): The URL to fetch and process. It should be a valid URL string.

    Returns:
        Dict[str, Any]: A dictionary with the URL as the key. The value is either:
            - An error message if there was an issue fetching the page (e.g., network error, invalid URL).
            - The processed data extracted from the HTML page, as returned by the `parse_html` function.
    """
    response = get_html(url)
    if response['error']:
        return {url: {'error': response['error']}}
    return {url: parse_html(url, response['html'])}

def extract_data_from_urls(urls: List[str], max_workers: int = 5) -> List[Dict[str, Any]]:

    """
    Extracts data from a list of URLs concurrently using parallel processing.

    This function takes a list of URLs and uses a thread pool to fetch and process each URL in parallel.
    The processing of each URL is handled by the `process_url` function, which is expected to return
    a dictionary containing the extracted data from the page. By using parallelism with threads, this
    function can significantly speed up the extraction process, especially when working with a large number
    of URLs.

    Args:
        urls (List[str]): A list of URLs (strings) to process. Each URL will be processed concurrently.
        max_workers (int, optional): The maximum number of threads to use for concurrent processing.
            Defaults to 5. Increasing this value can speed up processing, but may consume more system resources.
    
    Returns:
        List[Dict[str, Any]]: A list of dictionaries, where each dictionary contains the extracted data
        from one URL. The exact structure of the dictionary depends on the implementation of `process_url`.
    """
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        return list(executor.map(process_url, urls))



if __name__ == "__main__":
    urls = [
        'https://birgunjmun.gov.np/en',
        'https://mechinagarmun.gov.np/en',
        'https://melaulimun.gov.np/',
        'https://butwalmun.gov.np/',
    ]
    
    all_data = extract_data_from_urls(urls)
    
    for data in all_data:
        for url, services in data.items():
            print(f"URL: {url}")
            if isinstance(services, dict) and 'error' in services:
                print(f"Error: {services['error']}")
            else:
                for service in services:
                    print(f"Service Name: {service['service_name']}, "
                          f"Link: {service['link_of_service']}")
