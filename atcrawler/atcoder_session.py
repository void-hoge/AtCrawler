#!/usr/bin/env python3

import sys
import os
import re
import time
import getpass
import requests
from enum import Enum
from bs4 import BeautifulSoup

from atcrawler.utils import *

class AtCoderSession:
    def __init__(self):
        self.session = requests.Session()
        self.prev_request_time = time.time()
        try:
            self.load_session()
            print('The session loaded from cookies.', file=sys.stderr)
        except LoginFailedError:
            self.login()
            self.save_session()

    def verify_login(self):
        html = self.session.get('https://atcoder.jp').text
        if 'My Profile' not in html:
            return LoginFailedError

    def parse_csrf(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        return soup.find('form').find('input', type='hidden').get('value')

    def login(self):
        username = input('username: ')
        password = getpass.getpass('password: ')
        csrf = self.parse_csrf(self.session.get('https://atcoder.jp/login').text)
        data = {'username': username, 'password': password, 'csrf_token': csrf}
        response = self.session.post('https://atcoder.jp/login', data)
        if 'Forgot' in response.text:
            raise LoginFailedError

    def load_session(self):
        try:
            with open(f'{COOKIE_PATH}{COOKIE_FILE}', 'r') as f:
                for line in f:
                    name, value, domain, path = line.strip().split('\t')
                    cookie = requests.cookies.create_cookie(
                        name=name, value=value, domain=domain, path=path)
                    self.session.cookies.set_cookie(cookie)
        except:
            raise LoginFailedError
        self.verify_login()

    def save_session(self):
        try:
            os.makedirs(COOKIE_PATH)
        except:
            pass
        with open(f'{COOKIE_PATH}{COOKIE_FILE}', 'w') as f:
            for cookie in self.session.cookies:
                f.write(f'{cookie.name}\t{cookie.value}\t{cookie.domain}\t{cookie.path}\n')

    def get(self, url):
        now = time.time()
        if now - self.prev_request_time < REQUEST_INTERVAL:
            time.sleep(REQUEST_INTERVAL - (now - self.prev_request_time))
        response = self.session.get(url)
        self.prev_request_time = time.time()
        if response.status_code != 200:
            raise RequestFailedError(response.status_code)
        return response.text
