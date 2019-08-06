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


from distutils.core import setup
import pyiface

setup(name='PyIface', version=pyiface.__version__,
	description='Easy API for low-level wireless hardware system calls.',

	author=pyiface.__author__, author_email='bobafett2021@hotmail.com',
	license='Apache-2.0', url='https://github.com/PyDever/PyIface',
	packages=['pyiface'])


