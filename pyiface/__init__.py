#!/usr/bin/python2
# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 Kaleb Roscco Horvath
#
# Licensed under the Apache License, Version 2.0, (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#       (A copy should also be included with this source distribution)
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is done "AS IS",
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either expressed or implied.
# See the License for specific language governing permissions and
# limitations under the License.
#
# Violators of the License will be prosecuted following severe offences.

r"""PyIface - Easy API for low-level wireless hardware system calls

This package exports the following modules and subpackages:
	Interface - the public bound object that binds together all private API methods.

Since version 1.2.beta, PyIface implements the Interface object. Older applicants
of PyIface are HIGHLY ENCOURAGED to migrate.
"""

import logging, os

__author__ = 'Kaleb Roscoo Horvath'
__version__ = '1.2.beta'
__license__ = 'Apache-2.0'

__all__ = []


def __setup_log ():
	# setup logging according to
	# https://github.com/pyusb/pyusb
	pass


