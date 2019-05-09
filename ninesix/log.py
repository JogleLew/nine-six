#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Nine Six """
""" log.py """
""" Copyright 2019, Jogle Lew """

import os
import sys
import inspect
import logging
import ninesix.util as util

class Logger():
    def __init__(self, name, log_level=0, verbose=True, preserve=True):
        self.name = name
        self.log_level = log_level
        self.verbose = verbose
        self.preserve = preserve
        self.create_time = util.current_time()

    def log(self, message, tag="Log", log_level=1):
        # Get related information
        log_frame = inspect.stack()[1]
        cur_time = util.current_time()
        file_name = log_frame.filename
        base_name = os.path.basename(file_name)
        line_number = log_frame.lineno
        function_name = log_frame.function
        code_context = log_frame.code_context

        if log_level > self.log_level:
            print("%s - %s [%s] (%s: %d in %s()):\n%s\n" % (cur_time, self.name, tag, base_name, line_number, function_name, message))
