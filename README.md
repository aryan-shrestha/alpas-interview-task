# eGovernance services scraper

In this project the goal is to extract information about the 'eGovernance services' offered by various municipalities through their official websites. Using Python web scraping libraries such as BeautifulSoup Scrapy or other relevant tools the task is to scrape and retrieve the specific eGovernance services provided by each municipality.

## Requirement

[Click here to view the task requirements](https://drive.google.com/file/d/1NWUv9DGKAnAl4fKXljWSOsIwhpxogUHE/view?usp=sharing)

## Installation

#### Clone the repo

```
$ git clone https://github.com/aryan-shrestha/alpas-interview-task.git
```

#### Create a virtual environment

```
$ python3 -m venv venv
```

#### Install dependencies

```
$ pip install -r requirements.txt
```

#### Run directly from utils.py

```
python -u "path to /eGovServiceScraper/scraper/utils.py"
```

#### Or use the API built using Django REST Framework

```
python manage.py runserver
```

## Demo

#### Endpoint: /api/scrapper/

#### Method: POST

#### Payload:

```
{

"urls"  :  [

	"https://butwalmun.gov.np/",

	"https://biratnagarmun.gov.np/",
	]
}
```

#### Response:

```
[
	{
		"https://butwalmun.gov.np/":  [
			{
				"service_name":  "विद्युतीय सुशासन सेवाहरु",
				"link_of_service":  "/"
				},
			{
				"service_name":  "अनलाइन राजस्व भुक्तानि",
				"link_of_service":  "https://eservice.butwalmun.gov.np/"
			},
			{
				"service_name":  "नक्शापास (EBPS)",
				"link_of_service":  "http://ebps.butwalmun.gov.np/"
			},
			{
				"service_name":  "House Numbering",
				"link_of_service":  "http://map.butwalmun.gov.np/"
			}
		]
	},
	{
		"https://biratnagarmun.gov.np/":  [
			{
				"service_name":  "विधुतीय शुसासन सेवा",
				"link_of_service":  "/ne"
			},
			{
				"service_name":  "अनलाईन कर भुक्तानी प्रणाली",
				"link_of_service":  "https://eservice.biratnagarmun.gov.np/"
			},
			{
				"service_name":  "अनलाइन घटना दर्ता निवेदन",
				"link_of_service":  "https://public.donidcr.gov.np/"
			},
			{
				"service_name":  "एकिकृत विपद् पोर्टल",
				"link_of_service":  "http://biratnagarmun.bipadportal.gov.np/"
			},
			{
				"service_name":  "विराटनगर दुर शिक्षा कार्यक्रम-२०७७",
				"link_of_service":  "/ne/content/%E0%A4%B5%E0%A4%BF%E0%A4%B0%E0%A4%BE%E0%A4%9F%E0%A4%A8%E0%A4%97%E0%A4%B0%E0%A4%A6%E0%A5%81%E0%A4B0-%E0%A4%B6%E0%A4%BF%E0%A4%95%E0%A5%8D%E0%A4%B7%E0%A4%BE-%E0%A4%95%E0%A4%BE%E0%A4%B0%E0%A5%8D%E0%A4%AF%E0%A4%95%E0%A5%8D%E0%A4%B0%E0%A4%AE%E0%A5%A8%E0%A5%A6%E0%A5%AD%E0%A5%AD"
			}
		]
	}
]
```
