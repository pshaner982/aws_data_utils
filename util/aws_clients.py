#!/usr/bin/env python
# encoding: utf-8
"""
aws_clients.py
util/aws_clients.py

Created by Patrick Shaner 2021-06-10

Copyright (c) 2021 Patrick Shaner, All rights reserved
THE INFORMATION CONTAINED HEREIN IS PROPRIETARY AND CONFIDENTIAL

Generic utility that can be used for creating boto3 client connections.
Is platform aware and on Windows will disable ssl verification.

Version 2021-06-10:
    Initial file creation
"""
import boto3
import platform


__all__ = ["s3_client", "glue_client", "sns_client"]


def s3_client() -> boto3.client:
    """Leverages boto3 to creating an instance of client initialized to S3

    Returns:
        boto3.client
    """
    if platform.system().lower() == "windows":
        client = boto3.client("s3", verify=False)
    else:
        client = boto3.client("s3")
    return client


def glue_client() -> boto3.client:
    """Leverages boto3 to creating an instance of client initialized to glue

    Returns:
        boto3.client
    """
    if platform.system().lower() == "windows":
        client = boto3.client("glue", verify=False)
    else:
        client = boto3.client("glue")
    return client


def sns_client() -> boto3.client:
    """Creates the connection to sns utilizing boto3.  If on windows will set the verify to false
    Returns:
        boto3.client
    """
    if platform.system().lower() == "windows":
        client = boto3.client("sns", verify=False)
    else:
        client = boto3.client("sns")
    return client
