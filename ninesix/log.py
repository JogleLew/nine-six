#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Nine Six """
""" log.py """
""" Copyright 2019, Jogle Lew """

import os
import sys
import json
import inspect
import logging
import traceback
import threading
import ninesix.util as util
from ninesix.writer import StdoutWriter, JSONWriter

def log_except_hook(*exc_info):
    logger = Logger.logger
    text = "".join(traceback.format_exception(*exc_info))
    logger.msg(text, tag="Exception")
sys.excepthook = log_except_hook


class Logger():
    logger = None

    def __init__(self, name, log_level=0, verbose=True, preserve=True):
        self._lock = threading.Lock()
        self.name = name
        self.log_level = log_level
        self.verbose = verbose
        self.preserve = preserve
        self.create_time = util.current_time()
        self.watch_pgs = {}
        self.watch_val = {}
        self.daos = []
        if verbose:
            self.daos.append(StdoutWriter())
        if preserve:
            config = util.get_config()
            if config["storage_mode"] == "json":
                self.daos.append(JSONWriter(config, name, self.create_time))
        self.msg("Logger [%s] Initialized." % name)
        Logger.logger = self

    def config(self, cfg, fmt, tag="Log", log_level=1):
        self._lock.acquire()
        if log_level > self.log_level:
            log_frame = inspect.stack()[1]
            cur_time = util.current_time()

            # config object to json
            if fmt == "json":
                config_json = cfg
            elif fmt == "argparse":
                config_json = vars(cfg)

            # config hijack
            if "NINESIX_CONFIG" in os.environ:
                new_cfg = json.loads(os.environ["NINESIX_CONFIG"])
                config_json.update(new_cfg)
                if fmt == "json":
                    cfg.update(new_cfg)
                elif fmt == "argparse":
                    cfg = util.json_to_object(json.dumps(config_json))

            for dao in self.daos:
                dao.config(config_json, log_frame, cur_time, tag)
        self._lock.release()
        return cfg

    def msg(self, message, tag="Log", log_level=1):
        self._lock.acquire()
        if log_level > self.log_level:
            log_frame = inspect.stack()[1]
            cur_time = util.current_time()
            for dao in self.daos:
                dao.msg(str(message), log_frame, cur_time, tag)
        self._lock.release()

    def progress(self, label, cur_pgs, total=None):
        self._lock.acquire()
        if not label in self.watch_pgs:
            self.watch_pgs[label] = {}
        self.watch_pgs[label]["current"] = cur_pgs
        if total is not None:
            self.watch_pgs[label]["max"] = total
        self._lock.release()

    def unwatch(self, label):
        self._lock.acquire()
        if label in self.watch_pgs:
            del self.watch_pgs[label]
        elif label in self.watch_val:
            del self.watch_val[label]
        self._lock.release()

    def value(self, cur_dict, tag="Log", log_level=1):
        self._lock.acquire()
        if log_level > self.log_level:
            log_frame = inspect.stack()[1]
            cur_time = util.current_time()
            for label, cur_val in cur_dict.items():
                self.watch_val[label] = cur_val
            for dao in self.daos:
                dao.value(cur_dict, self.watch_pgs, self.watch_val, log_frame, cur_time, tag)
        self._lock.release()
