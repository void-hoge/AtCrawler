#!/usr/bin/env python3

import sys
from atcrawler.atcoder_session import AtCoderSession
from atcrawler.submission_collector import SubmissionCollector

def main():
    session = AtCoderSession()
    collector = SubmissionCollector(session, sys.argv[1])
    collector.collect(username=sys.argv[2])
