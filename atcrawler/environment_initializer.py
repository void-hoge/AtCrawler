#!/usr/bin/env python3

import sys
import os
import re
import time
import getpass
import requests
import html
from enum import Enum
from bs4 import BeautifulSoup

from atcrawler.utils import *

class EnvironmentInitializer:
    def __init__(self, session, contest):
        self.session = session
        self.contest = contest.lower()
        self.url = f'https://atcoder.jp/contests/{self.contest}'
        print(f'{self.contest.upper()} ({self.url} )', file=sys.stderr)
        self.tasks = self.get_tasks()

    def build(self):
        self.create_directories(self.tasks)
        self.create_samples(self.tasks)

    def get_tasks(self):
        page = self.session.get(f'{self.url}/tasks')
        soup = BeautifulSoup(page, 'html.parser')
        tasks = {}
        for link in soup.find_all('a'):
            if link.get('href'):
                match = re.search(
                    f'/contests/{self.contest}/tasks/{self.contest}_([a-z])',
                    link.get('href'))
                if match and len(link.get_text()) != 1:
                    print(f'{match.group(1).upper()}: {link.get_text()}', file=sys.stderr)
                    sanitized = self.sanitize_title(link.get_text())
                    tasks[match.group(1)] = {
                        'title': link.get_text(),
                        'sanitized': sanitized,
                        'dirname': f'{self.contest}/{match.group(1).upper()}-{sanitized}',
                        'link': f'https://atcoder.jp{link.get("href")}'}
        return tasks

    def sanitize_title(self, title):
        result = ''
        for ch in title.lower().strip():
            if ch in 'abcdefghijklmnopqrstuvwxyz0123456789.':
                result += ch
            else:
                result += '-'
        return result

    def create_directories(self, tasks):
        for prefix, task in tasks.items():
            print(f'Creating directory for task {prefix.upper()}...', file=sys.stderr)
            try:
                os.makedirs(f'{task["dirname"]}')
            except FileExistsError:
                pass

    def create_samples(self, tasks):
        for prefix, task in tasks.items():
            print(f'Downloading and parsing samples for task {prefix.upper()}...', file=sys.stderr)
            page = self.session.get(f'{task["link"]}')
            samples = self.parse_samples(page)
            for idx, sample in enumerate(samples):
                with open(f'{task["dirname"]}/test{idx+1}', 'w') as f:
                    f.write(sample['input'])
                with open(f'{task["dirname"]}/exp{idx+1}', 'w') as f:
                    f.write(sample['output'])

    def parse_samples(self, page):
        lines = page.split('\n')
        INPUT_START_RE = r'<h[0-9]+>Sample Input ([0-9]+)</h[0-9]+><pre>(.+)'
        INPUT_END_RE = r'</pre>'
        OUTPUT_START_RE = r'<h[0-9]+>Sample Output ([0-9]+)</h[0-9]+><pre>(.+)'
        OUTPUT_END_RE = r'</pre>'
        inputs = []
        outputs = []
        state = 'init'
        for line in lines:
            line = line.replace('\r', '')
            if state == 'init':
                match = re.search(INPUT_START_RE, line)
                if match:
                    inputs.append(html.unescape(match.group(2)))
                    state = 'input'
                    continue
                match = re.search(OUTPUT_START_RE, line)
                if match:
                    outputs.append(html.unescape(match.group(2)))
                    state = 'output'
                    continue
            elif state == 'input':
                if re.search(INPUT_END_RE, line):
                    state = 'init'
                    inputs[-1] += '\n'
                    continue
                else:
                    inputs[-1] += '\n' + html.unescape(line)
            elif state == 'output':
                if re.search(OUTPUT_END_RE, line):
                    state = 'init'
                    outputs[-1] += '\n'
                    continue
                else:
                    outputs[-1] += '\n' + html.unescape(line)
        samples = []
        for i, o in zip(inputs, outputs):
            samples.append({'input': i, 'output': o})
        return samples
