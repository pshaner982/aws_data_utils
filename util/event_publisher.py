#!/usr/bin/env python
# encoding: utf-8
"""
event_publisher.py
util/event_publisher.py

Created by Patrick Shaner 2021-06-10

Copyright (c) 2021 Patrick Shaner, All rights reserved
THE INFORMATION CONTAINED HEREIN IS PROPRIETARY AND CONFIDENTIAL

Helper for logging that publishes events to SNS topics.
To utilize the functionality the ENV variable 'EVENT_TOPIC'

Version 2021-06-10
    Created for custom logging.
"""

"""
level, msg, args, exc_info=None, extra=None, stack_info=False,
             stacklevel=1
"""
def _send_message_to_sns(self, body: str, attr: dict, topic: str):
    """Sends the message to the required topic.
    Args:
        body (str): message details.
        attr (dict): formatted message attributes for SNS publish
        topic (str): SNS topic name to send message too
    Returns:
        None
    """
    if not self._sns_client:
        self._set_sns_client()
    response = self._sns_client.publish(TopicArn=topic, Message=body, MessageAttributes=attr)
    print(response)

    def _format_sns_message(self, level: str, message: str, snow_team: str) -> tuple:
        """Takes details from the log level to format the message attributes and message for the SNS publish call.
        Args:
            level (str): Should be the same as the call point
            message (str): string value to be stored as free text
            snow_team (str): destination for SNOW integration
        Returns:
            tuple: message_attributes (dict), message_body(dict)

        """
        trace = "".join(traceback.format_list(traceback.extract_stack()[:-2]))
        time_stamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())

        attr = {
            "team": {
                "DataType": "string",
                "StringValue": self._team
            },
            "module": {
                "DataType": "string",
                "StringValue": self._module
            },
            "traceback": {
                "DataType": "string",
                "StringValue": trace
            },
            "utc_time_stamp": {
                "DataType": "string",
                "StringValue": time_stamp
            },
            "message_type": {
                "DataType": "string",
                "StringValue": level
            },
            "message": {
                "DataType": "string",
                "StringValue": message
            },
            "snow_team": {
                "DataType": "string",
                "StringValue": snow_team
            }
        }
        body = {
            "team": self._team,
            "module": self._module,
            "traceback": trace,
            "utc_time_stamp": time_stamp,
            "message_type": level,
            "message": message,
            "snow_team": snow_team
        }
        return attr, body