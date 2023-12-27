#!/usr/bin/env python3

import sys
import os
import re
import time
import getpass
import requests
from enum import Enum
from bs4 import BeautifulSoup

COOKIE_PATH = f'{os.environ["HOME"]}/.local/share/atcrawler/'
COOKIE_FILE = 'cookie.txt'

LANGUAGE_SUFFIX = {
    'C++': 'cpp',
    'Python': 'py',
    'Java': 'java',
    'Rust': 'rs',
    'C': 'c',
    'C#': 'cs',
    'Kotlin': 'kt'
}

REQUEST_INTERVAL = 0.5

class SubmissionOrder(Enum):
    created = 'created'
    score = 'score'
    length = 'source_length'
    time = 'time_consumption'
    memory = 'memory_consumption'

class LoginFailedError(RuntimeError):
    pass

class CookieNotFoundError(RuntimeError):
    pass

class RequestFailedError(RuntimeError):
    pass

