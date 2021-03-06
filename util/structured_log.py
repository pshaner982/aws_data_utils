#!/usr/bin/env python
# encoding: utf-8
"""
custom_logger.py

Created by Patrick Shaner 2021-04-21

Copyright (c) 2021 Patrick Shaner, All rights reserved
THE INFORMATION CONTAINED HEREIN IS PROPRIETARY AND CONFIDENTIAL

Initialization of a structured logging utility with connection to sns to dispatch exception modules

Version 2021-04-21:
    Created for custom logging.
"""
import json
import logging
import os
import time


class StructLogs(object):

    _logger = None
    _level = None
    _team: str = None
    _module: str = None
    _name: str = None
    _utc_time = time.gmtime
    _format: logging.Formatter = None
    _failure_topic: str = None

    def __init__(self, module: str, team: str = None, level=10) -> None:
        """Created to generate a custom logging adaptor that will allow connect to a SNS topic and allow publishing
        to that topic.
        Args:
            team (str): team or group designing the module
            module (str): this should be dot separated
        Returns:
            None
        """
        self._team = team.lower()
        self._module = module.lower()
        self._failure_topic = os.getenv("SNS_FAILURE", None)
        filename = f"{self._team}.{self._module}"
        self._logger = logging.getLogger(filename)
        self._level = logging.getLevelName(level)
        self._logger.setLevel(self._level)
        self._set_formatter()
        self._add_stream_handler()

    @property
    def get_struct_format(self) -> dict:
        """Defines the keys and values for the structured logging format
        Returns:
            None
        """
        return {
            "team": self._team,
            "module": self._module,
            "utc_time_stamp": "%(asctime)s",
            "message_type": "%(levelname)s",
            "message": "%(message)s"}

    def _set_formatter(self) -> None:
        """Creates the logging format object that will be added to the stream handler

        Returns:
            None
        """
        self._format = logging.Formatter(fmt=json.dumps(self.get_struct_format), datefmt="%Y-%m-%d %H:%M:%S")
        self._format.converter = self._utc_time

    def _add_stream_handler(self):
        ch = logging.StreamHandler()
        ch.setFormatter(self._format)
        ch.setLevel(self._level)
        self._logger.addHandler(ch)

    def status(self, msg, *args, **kwargs):
        """
        Delegate an error call to the underlying logger.
        """
        self._logger.log(logging.INFO, msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        """
        Delegate a debug call to the underlying logger.
        """
        self._logger.log(logging.DEBUG, msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        """
        Delegate an info call to the underlying logger.
        """
        self._logger.log(logging.INFO, msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        """
        Delegate a warning call to the underlying logger.
        """
        self._logger.log(logging.WARNING, msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        """
        Delegate an error call to the underlying logger.
        """
        self._logger.log(logging.ERROR, msg, *args, **kwargs)

    def exception(self, msg, *args, exc_info=True, **kwargs):
        """
        Delegate an exception call to the underlying logger.
        """
        snow_team = kwargs.pop("destination", "developer")
        if self._failure_topic:
            message_attr, message_body = self._format_sns_message(level="exception", message=msg,
                                                                  snow_team=snow_team)
            self._send_message_to_sns(body=json.dumps(message_body), attr=message_attr, topic=self._failure_topic)

        self._logger.log(logging.ERROR, msg, *args, exc_info=exc_info, **kwargs)

    def critical(self, msg, *args, **kwargs):
        """
        Delegate a critical call to the underlying logger.
        """
        self._logger.log(logging.CRITICAL, msg, *args, **kwargs)




