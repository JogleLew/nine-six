#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Nine Six """
""" stdout_writer.py """
""" Copyright 2019, Jogle Lew """

import os
import sys
import ninesix.util as util

class StdoutWriter():
    def __init__(self, assign_width=-1):
        self.dirty = True
        self.last_len = 0
        self.last_width = -1
        self.assign_width = assign_width

    def _get_width(self):
        try:
            width = os.get_terminal_size().columns
            if width < 10:
                width = 10
        except:
            width = 50
        if self.assign_width > 0:
            width = self.assign_width
        if not self.last_width == width:
            self.dirty = True
        self.last_width = width
        return width

    def config(self, config_json, log_frame, cur_time, tag):
        file_name = log_frame.filename
        base_name = os.path.basename(file_name)
        line_number = log_frame.lineno
        function_name = log_frame.function
        code_context = log_frame.code_context
        message = util.json_prettify(config_json)
        self.dirty = True

        sys.stdout.write("%s [%s] (%s: %d in %s()):\n%s\n\n" % (cur_time, tag, base_name, line_number, function_name, message))
        sys.stdout.flush()

    def msg(self, message, log_frame, cur_time, tag):
        file_name = log_frame.filename
        base_name = os.path.basename(file_name)
        line_number = log_frame.lineno
        function_name = log_frame.function
        code_context = log_frame.code_context
        self.dirty = True

        sys.stdout.write("%s [%s] (%s: %d in %s()):\n%s\n\n" % (cur_time, tag, base_name, line_number, function_name, message))
        sys.stdout.flush()

    def value(self, cur_dict, watch_pgs, watch_val, log_frame, cur_time, tag):
        width = self._get_width()
        file_name = log_frame.filename
        base_name = os.path.basename(file_name)
        line_number = log_frame.lineno
        function_name = log_frame.function
        code_context = log_frame.code_context
        message = self._val_message(watch_pgs, watch_val)
        content = self._fix_length("%s [%s] (%s: %d in %s()):" % (cur_time, tag, base_name, line_number, function_name), width, 1) + message + " " * width
        if not self.dirty:
            sys.stdout.write("\b" * self.last_len)
            sys.stdout.write(" " * self.last_len)
            sys.stdout.write("\b" * self.last_len)
        else:
            print("\n")
        sys.stdout.write(content)
        sys.stdout.flush()
        self.dirty = False
        self.last_len = len(content)

    def _fix_length(self, word, fix_len, mode):
        return ' ' * (fix_len - len(word)) + word if mode == 0 else word + ' ' * (fix_len - len(word))

    def _val_message(self, watch_pgs, watch_val):
        width = self._get_width()
        message = ""

        # print progress data
        if len(watch_pgs) > 0:
            label_maxlen = 0
            value_maxlen = 0
            for label, item in watch_pgs.items():
                if len(label) > label_maxlen:
                    label_maxlen = len(label)
                value_len = len(str(item["current"]))
                if "max" in item:
                    value_len += len(str(item["max"])) + 3
                if value_len > value_maxlen:
                    value_maxlen = value_len
            column_num = width // (label_maxlen + value_maxlen + 4)
            if column_num < 1:
                column_num = 1
            line_str = ""
            for idx, (label, item) in enumerate(watch_pgs.items()):
                value_str = str(item["current"])
                if "max" in item:
                    value_str += " / " + str(item["max"])
                line_str +=  "%s: %s  " % (
                    self._fix_length(label, label_maxlen, 1),
                    self._fix_length(value_str, value_maxlen, 1)
                )
                if (idx + 1) % column_num == 0:
                    message += self._fix_length(line_str, width, 1)
                    line_str = ""
            if len(watch_pgs) % column_num > 0:
                message += self._fix_length(line_str, width, 1)

        if len(watch_pgs) > 0 and len(watch_val) > 0:
            message += "-" * width

        # print value data
        if len(watch_val) > 0:
            label_maxlen = 0
            value_maxlen = 0
            for label, item in watch_val.items():
                if len(label) > label_maxlen:
                    label_maxlen = len(label)
                if len(str(item)) > value_maxlen:
                    value_maxlen = len(str(item))
            column_num = width // (label_maxlen + value_maxlen + 4)
            if column_num < 1:
                column_num = 1
            line_str = ""
            for idx, (label, item) in enumerate(watch_val.items()):
                line_str +=  "%s: %s  " % (
                    self._fix_length(label, label_maxlen, 1),
                    self._fix_length(str(item), value_maxlen, 1)
                )
                if (idx + 1) % column_num == 0:
                    message += self._fix_length(line_str, width, 1)
                    line_str = ""
            if len(watch_val) % column_num > 0:
                message += self._fix_length(line_str, width, 1)

        return message
