import requests
import json


class Amadeus:
    """
    Amadeus Travel APIs connect you to the richest information in the travel industry.
    https://developers.amadeus.com/
    """

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
    test_keys_json = 'test_keys.json'
    covid19_restrictions_json = 'covid19_restrictions.json'

    def __init__(self):
        self.authorization_header_value = None
        self.api_key = None
        self.api_secret = None

    def load_test_keys(self):
        with open(self.test_keys_json) as f:
            test_keys = json.load(f)
            self.api_key = test_keys['api_key']
            self.api_secret = test_keys['api_secret']

    def authorize(self):
        """
        implementation of https://developers.amadeus.com/self-service/apis-docs/guides/authorization-262
        """
        data = f'grant_type=client_credentials&client_id={self.api_key}&client_secret={self.api_secret}'
        url = 'https://test.api.amadeus.com/v1/security/oauth2/token'
        headers = {
            'User-Agent': self.user_agent,
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.post(url, headers=headers, data=data)
        auth = response.json()
        self.authorization_header_value = f'{auth["token_type"]} {auth["access_token"]}'

    def dump_restrictions(self, restrictions: str):
        with open(self.covid19_restrictions_json, 'w', encoding='utf-8') as f:
            f.write(restrictions)

    def get_covid19_restrictions(self, country_code: str) -> str:
        """
        Covid-19 Area Report
        :param country_code: ISO 3166 Alpha-2 code. e.g. "US" United States of America.
        :return: Covid-19 restrictions on targeted area
        """
        url1 = 'https://test.api.amadeus.com/v1'
        url2 = '/duty-of-care/diseases/covid19-area-report'
        url = f'{url1}{url2}'
        params = {'countryCode': country_code}
        headers = {'Authorization': self.authorization_header_value}
        response = requests.get(url, params=params, headers=headers)
        self.dump_restrictions(response.text)
        return response.json()['data']['summary']


if __name__ == '__main__':
    amadeus = Amadeus()
    amadeus.load_test_keys()
    amadeus.authorize()
    restrictions = amadeus.get_covid19_restrictions("US")
    print(restrictions)
