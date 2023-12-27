#!/usr/bin/env python3

from atcrawler.atcoder_session import AtCoderSession
from atcrawler.environment_initializer import EnvironmentInitializer
from atcrawler.submission_collector import SubmissionCollector


def main():
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('mode', type=str, choices=['init', 'crawl'],
                        help='Specify the mode, (init: inintialize environment, crawl: initialize environment and download submissions)')
    parser.add_argument('contest', type=str,
                        help='Specify the contest name.')
    parser.add_argument('--username', '-u',
                        required=False, default='',type=str,
                        help='When crawl mode, specify the author.')
    parser.add_argument('--language', '-l',
                        required=False, default='', type=str,
                        help='When crawl mode, specify the language.')
    parser.add_argument('--task', '-t',
                        required=False, default='', type=str,
                        choices=list('abcdefghijklmnopqrstuvwxyz'), help='When crawl mode, specify the task (a-z).')
    parser.add_argument('--result', '-r',
                        required=False, default='',
                        type=str, help='When crawl mode, specify the submission result.')
    parser.add_argument('--orderby', '-o',
                        required=False, default='', type=str,
                        choices=['created', 'score', 'source_length', 'time_consumption', 'memory_consumption'],
                        help='When crawl mode, specify the order.')
    parser.add_argument('--desc', '-d',
                        required=False, default=False, type=bool,
                        help='When crawl mode, set when descending order.')
    parser.add_argument('--maxsubmissions', '-m',
                        required=False, default=20, type=int,
                        help='When crawl mode, the max submissions number.')
    args = parser.parse_args()
    session = AtCoderSession()
    if args.mode == 'init':
        env = EnvironmentInitializer(session, args.contest)
        env.build()
    elif args.mode == 'crawl':
        collector = SubmissionCollector(session, args.contest)
        collector.collect(username=args.username,
                          language=args.language,
                          task=args.task,
                          result=args.result,
                          orderby=args.orderby,
                          descending=args.desc,
                          maxsubmissions=args.maxsubmissions)
    # session = AtCoderSession()
    # collector = SubmissionCollector(session, sys.argv[1])
    # collector.collect(username=sys.argv[2])
