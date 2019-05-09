#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Nine Six """
""" util.py """
""" Copyright 2019, Jogle Lew """

import os
import json
import datetime

default_config = {
    "storage_mode": "json"
}


def current_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_config():
    config_file = os.path.join(os.path.expanduser("~"), ".ninesix")
    if not os.path.isfile(config_file):
        with open(config_file, "w") as f:
            f.write(json.dumps(default_config, sort_keys=True, indent=4, separators=(',', ':'), ensure_ascii=False))
            return default_config
    with open(config_file, "r") as f:
        config = json.loads(f.read())
        return config
