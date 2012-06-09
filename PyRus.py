#!/usr/bin/env python
import PyRus
import argparse, os.path
from PyRus import *
from pprint import pprint
from time import sleep
from datetime import datetime

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = "TODO")
    parser.add_argument('-V', '--version', action='version', version = '%(prog)s {}'.format(version))
    parser.add_argument('-u', '--url', help = "Url of a feed", action='append')
    parser.add_argument('-c', '--config', help = "Config file to use", default = "~/.rss_config")
    parser.add_argument('-s', '--sleep', help = "seconds to sleep between gets", default = None, type = int)
    parser.add_argument('-o', '--output', help = "output file", default = None)
    args = parser.parse_args()
    config_path = os.path.expanduser(args.config)
    config = read_config(config_path)
    processor = processing.Processor(config)
    url = args.url or config['url']
    output = args.output or config['output']
    print "Activate {url} => {output}".format(url = url, output = output)
    if args.sleep is not None:
        while True:
            feeds = get_feeds(url)
            gotten = rssxml.xml_string(processor.process(get_feeds(url)))
            with open(output, 'w') as f:
                f.write(gotten)
            print datetime.now()
            sleep(args.sleep)
    else:
        print (rssxml.xml_string(processor.process(get_feeds(url))))
