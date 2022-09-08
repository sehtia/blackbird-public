import pandas
import random
import requests
import time

class ApiScraper:
    """ Scrapes the API found in network console of target sites to scrape.

        This is the preferred option to scraping. Secondary is parsing HTMl on webpage if API requires auth
        or cannot be found.
    """

    COMPANY_FIELDS = [
        "Company Name",
        "Company Url",
        "Twitter Url",
        "Year Founded",
        "Industries",
        "Funding",
        "City",
        "Street Address"
    ]


    def __init__(self):
        self.session=requests.session()

    def scrape_to_csv(self, csv_file_path='company_data_builtin.csv'):
        company_data = self.scrape()
        staker_total_stats = pandas.DataFrame(company_data, columns=self.COMPANY_FIELDS)
        staker_total_stats.to_csv(csv_file_path, mode='a', header=True)

    def scrape(self):
        #Define API url
        url_search='https://sg-en-web-api.ezbuy.sg/api/EzCategory/ListProductsByCondition'

        url = 'https://api.builtin.com/graphql'
        #Define header for the post request
        headers={'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}
        # 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
        #Define payload for the request form
        # data={
        #     "searchCondition":
        #         {"categoryId":0,"freeShippingType":0,"filter": [],"keyWords":"mask"},
        #         "limit":100,
        #         "offset":0,
        #         "language":"en",
        #         "dataType":"new"
        #     }

        data = {"operationName":"GetFilteredCompanies","variables":{"pagination":{"perPage":20,"page":1},"filters":{"industries":["web3"]}},"query":"query GetFilteredCompanies($pagination: PaginatonInput = {}, $filters: CompanyFiltersInput = {}) {\n  filterCompanies(pagination: $pagination, filters: $filters) {\n    companies {\n      id\n      alias\n      mission\n      name\n      city\n      state\n      totalEmployees\n      url\n      offices {\n        city\n        state\n        headquarters\n      }\n      officeType\n}\n    total\n  }\n}\n"}
        company_names = set()
        company_data_result = []
        for page_number in range(1,10):
            time.sleep(max(random.gauss(1,0.5),2))
            data['variables']['pagination']['page'] = page_number
            req=self.session.post(url,headers=headers,json=data)
            print('req:', req)
            json_response = req.json()
            # print('json:', json_response)
            # return []
            companies = json_response['data']['filterCompanies']['companies']
            for company in companies:
                if company['name'] not in company_names:
                    company_names.add(company['name'])
                    alias = company['alias']
                    company_url_from_scraper = company['url']
                    if alias:
                        company_api_url = self.get_api_url(url, alias, company['city'], company['state'])
                        print("company_api_url being scraped:", company_api_url)
                        company_data = self.scrape_company(company_api_url)
                        if company_data:
                            company_data_result.append(company_data)
                            continue
                    else:
                        company_data_result.append((company["name"], "", "", "", [], [], "", ""))

                    # if self.is_end_of_result(company_url_from_scraper):
                    #     break

        print("COMPANY NAMES:", company_names)
        return company_data_result

    def is_end_of_result(self, url):
        return "/company/" not in url

    def get_api_url(self, url, alias, city, state):
        """
        input alias: '/company/eve-wealth'
        https://www.builtinnyc.com/company/republic
        https://api.builtin.com/companies/alias/fetchai?region_id=9
        URL to get region codes:
        https://www.builtincolorado.com/?state=eyJyZWZlcnJlZEJ5Ijoid3d3LmJ1aWx0aW5hdXN0aW4uY29tLyIsImNsaWVudElkZW50aWZpZXIiOiJleUpoYkdjaU9pSklVekkxTmlJc0luUjVjQ0k2SWtwWFZDSjkuZXlKcFpDSTZJalUxWkRBME1HVm1MVEEyTW1RdE5EaGtaUzA0T1dRNUxUa3laVFU0TmpFM09EZzFOeUo5LmdXQnRNU3VZZERoVDN0dnE3dE85UGRSUzR5TkZMNnVwaFZIVTR5ZnBxR2siLCJ1c2VyU2Vzc2lvbklkZW50aWZpZXIiOiI5MzQ1NzMyMS00MjM0LTQ4MDYtODVhNy0yZTExNmU2MjkwY2IifQ%253D%253D

        : {id: 4, name: "Austin", site_name: "Built In Austin", code: "austin", state: "TX", country: "USA",…}
        1: {id: 6, name: "Boston", site_name: "Built In Boston", code: "boston", state: "MA", country: "USA",…}
        2: {id: 1, name: "Chicago", site_name: "Built In Chicago", code: "chicago", state: "IL", country: "USA",…}
        3: {id: 2, name: "Colorado", site_name: "Built In Colorado", code: "colorado", state: "CO",…}
        4: {id: 3, name: "Los Angeles", site_name: "Built In LA", code: "la", state: "CA", country: "USA",…}
        5: {id: 5, name: "New York City", site_name: "Built In NYC", code: "nyc", state: "NY", country: "USA",…}
        6: {id: 8, name: "San Francisco", site_name: "Built In San Francisco", code: "san_francisco", state: "CA",…}
        7: {id: 7, name: "Seattle", site_name: "Built In Seattle", code: "seattle", state: "WA", country: "USA",…}

        """
        print("alias:", alias)
        print("url:", url)

        index_start = len("/company/")
        alias = alias[index_start:]
        region_id = 9
        if "chicago" in url or state == "IL":
            region_id = 1
        elif "colorado" in url or state == "CO":
            region_id = 2
        elif "builtinla" in url or city == "Los Angeles":
            region_id = 3
        elif "austin" in url or state == "TX":
            region_id = 4
        elif "builtinnyc" in url or state == "NY":
            region_id = 5
        elif "boston" in url or state == "BO":
            region_id = 6
        elif "seattle" in url or state == "WA":
            region_id = 7
        elif "francisco" in url or city == "San Francisco":
            region_id = 8

        return f"https://api.builtin.com/companies/alias/{alias}?region_id={region_id}"

    def scrape_company(self, company_url):
        # headers={'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}
        headers={'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
        req=self.session.get(company_url, headers=headers)
        if req.status_code != 200:
            print(f"Status code [{req.status_code}] with reason [{req.reason}]")
            return ()
        # print('req:', req.text)
        json_response = req.json()
        # print("json:", json_response)
        company_name = json_response['title']
        street_address = json_response['street_address_1']
        year_founded = json_response['year_founded']
        city = json_response['city']
        company_url = json_response['url']
        twitter_url = json_response['twitter']
        employee_count = max(json_response['local_employees'], json_response['total_employees'])
        industries = [industry_json['name'] for industry_json in json_response['industries'] if industry_json['name']]
        funding = [funding_json for funding_json in json_response['funding'] if funding_json['funding_amt']]

        return (company_name, company_url, twitter_url, year_founded, industries, funding, city, street_address)


def main():
    scraper = ApiScraper()
    print("scraper scraping")
    scraper.scrape_to_csv()
    # result = scraper.scrape_company("https://api.builtin.com/companies/alias/okcoin?region_id=9")
    # print("company deets", result)
if __name__ == "__main__":
    print("staaahting investigation misses hudson")
    main()