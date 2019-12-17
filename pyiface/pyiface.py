#!/usr/bin/python2
# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 Kaleb Roscco Horvath
#
# Licensed under the Apache License, Version 2.0, (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#	http://www.apache.org/licenses/LICENSE-2.0
#	(A copy should also be included with this source distribution)
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is done "AS IS",
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either expressed or implied.
# See the License for specific language governing permissions and
# limitations under the License.
#
# Violators of the License will be prosecuted following severe offences.


# standard library dependencies
try:
	import fcntl, struct, array
	import sys, os, socket, subprocess
except ImportError as e:
	sys.stdout.write('%s:%s' % (e.errno, e.errorstr)+'\n');
	sys.stdout.flush();
	sys.exit(1) # exit process in error state


# check platform id, and permissions
def __verify_POSIX_compliant ():
	"""Private bound method, checks that machine is POSIX compliant.

	:returns (bool): compliancy
	:returns (int): 1 upon exit, error state

	:raises OSError: safety net
	:raises ValueError: bad argument
	"""
	try:
		os_platform_name = str(os.name) + filter(str.isdigit, sys.platform)
		return 'posix' in os_platform_name

	except (OSError, ValueError) as e:
		sys.stdout.write('%s:%s' % (e.errno, e.errorstr)+'\n')
		sys.stdout.flush();
		sys.exit(1) # exit process in error state


def __verify_root_privileges ():
	"""Private bound method, checks for root.

	:returns (bool): root privileges
	:returns (int): 1 upon exit, error state

	:raises OSError: safety net for OS failure
	:raises subprocess.CalledProcessError: bad shell command
	"""
	try:
		privilege_level = subprocess.check_output(['whoami'])
		return 'root' in privilege_level

	except (OSError, subprocess.CalledProecessError) as e:
		sys.stdout.write('%s:%s' % (e.errno, e.errorstr)+'\n')
		sys.stdout.flush();
		sys.exit(1) # exit process in error state


"""Test verification methods.
if __verify_POSIX_compliant():
	print __verify_root_privileges()
"""

# ioctl command codes, borrowed from: github.com/bat-serjo/PyIface
SIOCGIFCONF = 0x8912
SIOCGIFHWADDR = 0x8927

# more go here
max_possible = 8

# determine size of arg (struct) for ioctl system call
if sys.maxsize > 2**32: struct_size = 40
else:
	struct_size = 32
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)



def __execute_SIOCGIFHWADDR (fileno, iface):
	"""Execute IOCTL call to get hardware address of specificed interface
	and parse the output buffer accordingly.

	:param (int) fileno: file descriptor for access to interface
	:param (str) iface: name of wireless interface

	:returns (str) hardware_address: hardware address (MAC) of specificed interface

	:raises OSError: safety net
	:raises IOError: upon improper IOCTL call
	:raises socket.error: upon improper argument
	"""
	global SIOCGIFHWADDR
	# check that fileno does not burden file table
	if 'int' not in str(type(fileno)):
		raise ValueError
	elif int(fileno) == int(open('/proc/sys/fs/file-max', 'r').readlines()[0]):
		raise OSError
	else: pass

	# execute simple ioctl command system call
	try:
		outbytes = fcntl.ioctl(fileno, SIOCGIFHWADDR, struct.pack('256s', iface[:15]))

	except (IOError, socket.error) as e:
		sys.stdout.write('%s:%s' % (e.errno, e.errorstr)+'\n')
		sys.exit(1) # exit in error state

	hwaddr = "".join(
		['%02x:' % ord(char) for char in outbytes[18:24]])[:-1]
	return hwaddr



def __execute_SIOCGIFCONF (fileno):
	"""Execute IOCTL call to get list of interfaces
	and parse the output buffer into an array.

	:param (int) fileno: file descriptor for access to interface

	:returns (list) ifaces: interfaces and inet addresses

	:raises OSError: safety net
	:raises IOError: upon improper IOCTL call
	:raises socket.error: upon improper argument
	"""
	global max_possible; global struct_size; global SIOCGIFCONF
	# check that fileno does not burden file table
	if 'int' not in str(type(fileno)):
		raise ValueError
	elif int(fileno) == int(open('/proc/sys/fs/file-max', 'r').readlines()[0]):
		raise OSError
	else: pass

	# construct output buffer size for IOCTL call return
	bytes = max_possible * struct_size; names = array.array('B', '\0' * bytes)

	# execute ioctl command system call
	outbytes = struct.unpack('iL', fcntl.ioctl(int(fileno), SIOCGIFCONF, struct.pack('iL', bytes, names.buffer_info()[0])))[0]
	while True:
		if outbytes == bytes: max_possible *= 2
		else: break
	name_strings = names.tostring()
	try:
		ifaces = [(name_strings[i:i+16].split('\0', 1)[0],
			socket.inet_ntoa(name_strings[i+20:i+24 ]))
			for i in range(0, outbytes, struct_size)]

	except (OSError, socket.error) as e:
		sys.stdout.write('%s:%s' % (e.errno, e.errorstr)+'\n')
		sys.stdout.flush();
		sys.exit(1) # close process in error state

	return ifaces


"""Public bound wrapper methods, no classes saves memory for system calls."""
def list_ifaces ():
	global s; return __execute_SIOCGIFCONF(s.fileno())

def hardware_address (iface):
	global s; return __execute_SIOCGIFHWADDR(s.fileno(), str(iface))



if __name__ == '__main__':
	sys.exit(0)
	'''
	for iface in list_ifaces():
		sys.stdout.write('%s : %s : %s' % (iface[0], iface[1], hardware_address(iface[0]))+'\n')
	sys.exit(0) # exit in success state
	'''

