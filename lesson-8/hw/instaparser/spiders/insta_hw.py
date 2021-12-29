import json
import scrapy
from scrapy.http import HtmlResponse
from typing import List
import re

from instaparser.items import InstaHwItem


class InstaHwSpider(scrapy.Spider):
    name = 'insta_hw'
    allowed_domains = ['instagram.com']

    start_urls = ['https://www.instagram.com/']
    inst_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    inst_login = 'Onliskill_udm'
    inst_pwd = '#PWD_INSTAGRAM_BROWSER:10:1638551736:AedQAFI0vAAYTOunJJUOmrJPoJO3A6MjtJf+QOH/3ovuYhh9eIlQNGUh2MDiWMtQL80BL3LJqk7DfHobv+o7STw2Qg6qLwcDSuHFLa+tiYoPvNwdkG6zno3Y6Pr/Et12HLssUesjh66gbKA/Regr'

    def __init__(self, usernames: List[str], **kwargs):
        super().__init__(**kwargs)
        self.usernames = usernames

    def errback_parse(self, failure):
        # log all failures
        # b'{"message":"checkpoint_required","checkpoint_url":"/challenge/AXHJpoj7oqaEivU56ekqb9limASPuP81OWwekk4QMuyKnY2DnlJIOP_UVfIPA6nf3OooGA/QJ45g90XrB/","lock":false,"flow_render_type":0,"status":"fail"}'
        pass

    def parse(self, response: HtmlResponse, **kwargs):
        """
        Отправляем запрос на логин, используя `csrf` с главной страницы, и
        сообщаем, что обработаем ответ в `login`.
        """
        csrf = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(self.inst_login_link,
                                 method='POST',
                                 callback=self.login,
                                 errback=self.errback_parse,
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
                    callback=self.parse_a_user
                )

    def parse_a_user(self, response: HtmlResponse):
        """ Получить данные пользователя a_user со страницы /{username}. """
        _sharedData_as_str = response.xpath('//*[contains(text(), "_sharedData")]')[0].get()[52:-10]
        j_user = json.loads(_sharedData_as_str)['entry_data']['ProfilePage'][0]['graphql']['user']
        user_id = j_user['id']
        a_user = {'_id': user_id, 'username': j_user['username'], 'photo': j_user['profile_pic_url']}

        follow_urls = [
            f'https://i.instagram.com/api/v1/friendships/{user_id}/following/?count=12',
            f'https://i.instagram.com/api/v1/friendships/{user_id}/followers/?count=12&search_surface=follow_list_page']
        for url in follow_urls:
            yield response.follow(
                url,
                headers={'User-Agent': 'Instagram 155.0.0.37.107'},
                callback=self.parse_b_users,
                cb_kwargs={'a_user': a_user}
            )

    def parse_b_users(self, response: HtmlResponse, a_user):
        """
        Получить b_users подписчиков или на кого подписан пользователь a_user.
        Определить пользователей подписчики или те, на кого подписан нужно из запроса
        по вхождению подстроки 'following' или 'followers'.
        """
        j_data = response.json()

        next_max_id = j_data.get('next_max_id')
        if next_max_id:
            user_id = a_user["_id"]
            yield response.follow(
                self.get_b_users_url(response.url, user_id, next_max_id),
                headers={'User-Agent': 'Instagram 155.0.0.37.107'},
                callback=self.parse_b_users,
                cb_kwargs={'a_user': a_user}
            )

        b_users = list(map(
            lambda user: {'_id': user['pk'], 'username': user['username'], 'photo': user['profile_pic_url']},
            j_data['users']))

        yield self.create_insta_hw_item(a_user, b_users, response.url)

    @staticmethod
    def get_b_users_url(response_url, user_id, next_max_id):
        if response_url.find('/following') != -1:
            return f'https://i.instagram.com/api/v1/friendships/{user_id}/following/?count=12&max_id={next_max_id}'
        if response_url.find('/followers') != -1:
            return f'https://i.instagram.com/api/v1/friendships/{user_id}/followers/?count=12&max_id={next_max_id}&search_surface=follow_list_page'

    @staticmethod
    def create_insta_hw_item(a_user, b_users, url) -> InstaHwItem:
        if url.find('/following') != -1:
            return InstaHwItem(user_a=a_user, following_users=b_users, follower_users=[])
        if url.find('/followers') != -1:
            return InstaHwItem(user_a=a_user, following_users=[], follower_users=b_users)
