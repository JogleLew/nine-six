#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Nine Six """
""" util.py """
""" Copyright 2019, Jogle Lew """

import os
import json
import datetime
from argparse import Namespace

home_dir = os.path.expanduser("~")
default_config = {
    "storage_mode": "json",
    "storage_option": {
        "storage_path": os.path.join(home_dir, "96log")
    }
}


def current_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def json_prettify(raw_json):
    return json.dumps(raw_json, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)


def json_to_object(data):
    return json.loads(data, object_hook=lambda d: Namespace(**d))


def get_config():
    global home_dir
    config_file = os.path.join(home_dir, ".ninesix")
    if not os.path.isfile(config_file):
        with open(config_file, "w") as f:
            f.write(json_prettify(default_config))
            return default_config
    config = {}
    with open(config_file, "r") as f:
        config = json.loads(f.read())
    return config
