#!/usr/bin/env python
import PyRus
import argparse, os.path
from PyRus import *
from pprint import pprint
from time import sleep
from datetime import datetime
from md5 import md5

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = PyRus.__doc__)
    parser.add_argument('-V', '--version', action='version', version = '%(prog)s {}'.format(version))
    parser.add_argument('-c', '--config', help = "Config file to use", default = "~/.rss_config")
    parser.add_argument('-s', '--sleep', help = "seconds to sleep between gets",
            default = 3600, type = int)
    args = parser.parse_args()
    config_path = os.path.expanduser(args.config)
    filter = read_config(config_path)
    with open(config_path) as f:
        config_hash = md5(f.read())

    while True:
        with open(config_path) as f:
            new_config_hash = md5(f.read())
        if new_config_hash != config_hash:
            config_hash = new_config_hash
            filter = read_config(config_path)

        filter(None)
        print datetime.now()
        sleep(args.sleep)
