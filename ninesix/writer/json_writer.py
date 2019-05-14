#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Nine Six """
""" json_writer.py """
""" Copyright 2019, Jogle Lew """

import os
import json

class JSONWriter():
    def __init__(self, config, name, create_time):
        if not "storage_path" in config["storage_option"]:
            raise Exception("Please specific storage path in storage option.")
        storage_path = config["storage_option"]["storage_path"]
        self._mkdir(storage_path)
        work_path = os.path.join(storage_path, name)
        self._mkdir(work_path)
        date, hms = create_time.split()
        hms = hms.replace(":", "")
        date_dir = os.path.join(work_path, date)
        self._mkdir(date_dir)
        self.filepath = os.path.join(date_dir, hms + ".json")
        self.file = open(self.filepath, "w")
        self._first_log(create_time)

    def __del__(self):
        self.file.close()

    def _mkdir(self, path):
        if not os.path.isdir(path):
            os.mkdir(path)

    def _first_log(self, create_time):
        self.file.write(json.dumps([{
            "type": "msg", 
            "tag": "Log",
            "time": create_time, 
            "content": "JSON Writer Initialized."
        }]))

    def _log(self, json_obj):
        pos = self.file.tell()
        self.file.seek(pos - 1, os.SEEK_SET)
        self.file.write(",\n")
        self.file.write(json.dumps(json_obj))
        self.file.write("]")

    def config(self, config_json, log_frame, cur_time, tag):
        msg_obj = {
            "type": "config", 
            "tag": tag,
            "time": cur_time, 
            "content": config_json
        }
        self._log(msg_obj)

    def msg(self, message, log_frame, cur_time, tag):
        msg_obj = {
            "type": "msg", 
            "tag": tag,
            "time": cur_time, 
            "content": message
        }
        self._log(msg_obj)

    def value(self, cur_dict, watch_pgs, watch_val, log_frame, cur_time, tag):
        msg_obj = {
            "type": "value", 
            "tag": tag,
            "time": cur_time, 
            "content": {
                "progress": watch_pgs,
                "value": cur_dict
            }
        }
        self._log(msg_obj)
