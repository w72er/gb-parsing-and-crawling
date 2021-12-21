import json
from pprint import pprint

import scrapy
from scrapy.http import HtmlResponse
from typing import List
import re


class InstaHwSpider(scrapy.Spider):
    name = 'insta_hw'
    allowed_domains = ['instagram.com']

    start_urls = ['https://www.instagram.com/']
    inst_login_link = '	https://www.instagram.com/accounts/login/ajax/'
    inst_login = 'Onliskill_udm'
    inst_pwd = '#PWD_INSTAGRAM_BROWSER:10:1638551736:AedQAFI0vAAYTOunJJUOmrJPoJO3A6MjtJf+QOH/3ovuYhh9eIlQNGUh2MDiWMtQL80BL3LJqk7DfHobv+o7STw2Qg6qLwcDSuHFLa+tiYoPvNwdkG6zno3Y6Pr/Et12HLssUesjh66gbKA/Regr'

    def __init__(self, usernames: List[str], **kwargs):
        super().__init__(**kwargs)
        self.usernames = usernames

    def parse(self, response: HtmlResponse, **kwargs):
        """
        Отправляем запрос на логин, используя `csrf` с главной страницы, и
        сообщаем, что обработаем ответ в `login`.
        """
        csrf = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(self.inst_login_link,
                                 method='POST',
                                 callback=self.login,
                                 formdata={'username': self.inst_login,
                                           'enc_password': self.inst_pwd},
                                 headers={'X-CSRFToken': csrf})

    @staticmethod
    def fetch_csrf_token(text: str):
        """ Get csrf-token for auth """
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    def login(self, response: HtmlResponse):
        j_data = response.json()
        if j_data.get('authenticated'):
            for username in self.usernames:
                yield response.follow(
                    f'/{username}',
                    callback=self.parse_user_by_username,
                    cb_kwargs={'username': username}
                )

    def parse_user_by_username(self, response: HtmlResponse, username: str):
        _sharedData_as_str = response.xpath('//*[contains(text(), "_sharedData")]')[0].get()[52:-10]
        j_user = json.loads(_sharedData_as_str)['entry_data']['ProfilePage'][0]['graphql']['user']
        user_id = j_user['id']
        user_a = {'_id': user_id, 'username': j_user['username'], 'photo': j_user['profile_pic_url']}
        print('user_a')
        pprint(user_a)

        following_url = f'https://i.instagram.com/api/v1/friendships/{user_id}/following/?count=12'
        yield response.follow(
            following_url,
            headers={'User-Agent': 'Instagram 155.0.0.37.107'},
            callback=self.following_user_parse,
            cb_kwargs={'user_a': user_a}
        )

    def following_user_parse(self, response: HtmlResponse, user_a):
        j_data = response.json()

        next_max_id = j_data.get('next_max_id')
        if next_max_id:
            user_id = user_a["_id"]
            yield response.follow(
                f'https://i.instagram.com/api/v1/friendships/{user_id}/following/?count=12&max_id={next_max_id}',
                headers={'User-Agent': 'Instagram 155.0.0.37.107'},
                callback=self.following_user_parse,
                cb_kwargs={'user_a': user_a}
            )

        following_users = map(
            lambda user: {'_id': user['pk'], 'username': user['username'], 'photo': user['profile_pic_url']},
            j_data['users'])

        result = {'user_a': user_a, 'following_users': list(following_users)}
        pprint(result)
        yield result  # todo: Item
