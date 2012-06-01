#!/usr/bin/env python
import PyRus
import argparse
from PyRus import *
from pprint import pprint

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = "TODO")
    parser.add_argument('-V', '--version', action='version', version = '%(prog)s {}'.format(version))
    args = parser.parse_args()
    print (rssxml.xml_string(processing.process(get_feeds(
        ['http://xkcd.org/atom.xml',
        'http://www.reddit.com/r/Poetry/comments/stbxy/learning_thursday_share_a_poetry_technique_with/.rss']))))
