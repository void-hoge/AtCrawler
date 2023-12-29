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
from atcrawler.environment_initializer import EnvironmentInitializer

class SubmissionCollector(EnvironmentInitializer):
    def __init__(self, session, contest):
        super().__init__(session, contest)
        self.build()

    def collect(self, task='', username='', language='', result='',
                orderby=None, descending=False, maxsubmissions=20):
        submission_ids = []
        taskkey = f'{self.contest}_{task}' if task else ''
        page = 1
        while len(submission_ids) < maxsubmissions:
            print(f'Downloading and parsing the {page}{["st", "nd", "rd"][(page % 10) - 1] if page % 10 in [1,2,3] else "th"} submission page...', file=sys.stderr)
            url = self.url_format(taskkey, username, language, result, orderby, descending, page)
            html = self.session.get(url)
            ids = self.parse_submission_table(html)
            submission_ids += ids
            page += 1
            if len(ids) == 0:
                break
        submission_ids = submission_ids[0:maxsubmissions]
        print(f'Detected {len(submission_ids)} submissions.', file=sys.stderr)
        for idx in submission_ids:
            html = self.session.get(f'{self.url}/submissions/{idx}')
            prefix, langsys, code = self.parse_submission(html)
            print(f'Writing {langsys} source code for task {prefix.upper()}.')
            code_suffix = ''
            for lang, suff in LANGUAGE_SUFFIX.items():
                if lang in langsys:
                    code_suffix = '.' + suff
                    break
            with open(f'{self.tasks[prefix]["dirname"]}/{idx}{code_suffix}', 'w') as f:
                f.write(code)

    def parse_submission(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        pretexts = soup.find_all('pre')
        code = None
        for text in pretexts:
            if text.get('id'):
                if 'submission-code' in text.get('id'):
                    code = text.get_text().replace('\r', '')
        links = soup.find_all('a')
        for link in links:
            try:
                match = re.search(f'/contests/{self.contest}/tasks/{self.contest}_([a-z])', link.get('href'))
                if match:
                    prefix = match.group(1)
                    break
            except:
                pass
        language = soup.find('th', string='Language').find_parent('tr')
        langsys = language.find('td').get_text()
        return prefix, langsys, code

    def parse_submission_table(self, html):
        submission_ids = []
        soup = BeautifulSoup(html, 'html.parser')
        links = soup.find_all('a')
        for link in links:
            if 'Detail' in link.get_text():
                match = re.search(f'/contests/{self.contest}/submissions/([0-9]+)', link.get('href'))
                if match:
                    submission_ids.append(match.group(1))
        return submission_ids

    def url_format(self, task='', username='', language='', result='',
                   orderby=None, descending=False, page=1):
        langkey = self.lang2key(language)
        if orderby:
            if descending:
                url = f'{self.url}/submissions?desc=true&f.Task={task}&f.LanguageName={langkey}&f.Status={result}&f.User={username}&orderBy={orderby}&page={page}'
            else:
                url = f'{self.url}/submissions?f.Task={task}&f.LanguageName={langkey}&f.Status={result}&f.User={username}&orderBy={orderby}&page={page}'
        else:
            url = f'{self.url}/submissions?f.Task={task}&f.LanguageName={langkey}&f.Status={result}&f.User={username}&page={page}'
        return url

    def lang2key(self, language=''):
        key = ''
        for ch in language:
            if ch == ' ':
                key += '+'
            elif ch in '+#':
                key += f'%{ord(ch):X}'
            else:
                key += ch
        return key
