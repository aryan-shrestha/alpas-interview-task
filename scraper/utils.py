import requests
import re
from bs4 import BeautifulSoup
from typing import List, Dict, Any

def get_html(url: str) -> Dict[str, Any]:
    """
    Fetches the HTML content of a given URL.
    Uses the requests library to perform a GET request.
    Handles exceptions and returns a dictionary with the URL, error (if any), and HTML content.
    Args:
        url (str): The URL to fetch HTML from.

    Returns:
        Dict[str, Any]: A dictionary containing the URL, error (if any), and HTML content.
    """
    response = {
        'url': url,
        'error': None,
        'html' : None
    }
    try:
        res = requests.get(url)
    except Exception as e:
        response['error'] = type(e).__name__
    else:
        response['html'] = res.text
    return response

def parse_html(html: str) -> List[Dict[str, Any]]:
    """
    Parses the HTML content and extracts relevant data.

    Args:
        html (str): The HTML content to parse.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing extracted data.
    """
    soup = BeautifulSoup(html, 'html.parser')
    services_div = soup.find('div', id='block-menu-menu-egov-services')
    if services_div is None:
        services_div = soup.find('a', text=re.compile('विधुतीय|विद्युतीय', re.IGNORECASE))

    if services_div is None:
        return []
    elif services_div.name == 'a':
        services_div = services_div.find_parent('li')

    links_in_services_div = services_div.find_all('a', href=True)
    
    links = [{
        'service_name': link.get_text(strip=True),
        'link_of_service': link['href'].strip()
    } for link in links_in_services_div if link.get_text(strip=True) and link['href']]

    return links

def extract_data_from_urls(urls: List[str]) -> List[Dict[str, Any]]:
    """
    Extracts data from a list of URLs.

    Args:
        urls (List[str]): A list of URLs to extract data from.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing extracted data.
    """
    all_data = []
    for url in urls:
        response = get_html(url)
        if response['error']:
            all_data.append({url: {'error': response['error']}})
        else:
            data = parse_html(response['html'])
            all_data.append({url: data})
    
    return all_data


if __name__ == "__main__":
    urls = [
        'https://birgunjmun.gov.np/en',
        'https://mechinagarmun.gov.np/en',
        'https://melaulimun.gov.np/',
        'https://butwalmun.gov.np/',
    ]
    all_data = extract_data_from_urls(urls)
    # printing the data in a readable format
    for data in all_data:
        for url, services in data.items():
            print(f"URL: {url}")
            if 'error' in services:
                print(f"Error: {services['error']}")
            else:
                for service in services:
                    print(f"Service Name: {service['service_name']}, Link: {service['link_of_service']}")
            print("\n")