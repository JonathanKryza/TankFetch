# Copyright 2013 Jonathan Kryza. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import telnetlib
import datetime

ip = ''             			# The IP address of the ATG device you are polling.
port = 10001                    # The default for most ATG devices is 10001.
command = 'i201'               	# Go to the docs folder for a full listing of commands or visit https://www.veeder.com
tank = '00'                   	# '00' means ALL. For a specific tank, enter as follows: Tank 1 = "01", Tank 12 = "12", etc
log_file = 'logs.txt'			# Where captured output will be stored.


def fetch_atg(ip: str, port: int, command: str, data: str) -> bytes:
	"""
	Function for executing a command on an ATG unit and returning the output.

	ip - The IP address of the ATG device you are polling. String.\n
	port - The port used to remotely connect to the ATG's software. Integer.\n
	command - The command to execute on the ATG device (e.g. i201). String.\n
	data - Data to be appended to the end of the command (e.g. 00). String.
	"""

	# Initializes connection to ATG device.
	try:
		tn = telnetlib.Telnet(ip, port)
	except:
		return f'Failed to connect to host {ip} using port {port}.'

	# Converts payload to bytes and adds start of header CTRL + A to payload.
	payload = bytes(command + data, 'utf-8')
	tn.write(b'\x01' + payload)

	# Passes over the original payload in the output to get to the data.
	tn.read_until(payload)

	# Saves all output data prior to the end of transmission, removes ETX (CTRL + C).
	capture = tn.read_until(b'\x03', 10)
	capture = capture.replace(b'\x03', b'')

	# Closes connection and returns the captured data.
	tn.close()
	return capture
	

def report_txt(file: str, capture: bytes) -> None:	
	"""
	Used to record the captured data in a text file.

	file - The  file to store captured data in. String.
	capture - The captured data from fetch_atg(). Bytes.
	"""
	
	# Convert the captured bytecode data into a string.
	capture = capture.decode("utf-8")

	# Store current date.
	now = datetime.datetime.now()
	date = now.strftime('%m-%d-%Y')

	# Open the logs file and add the capture data.
	with open(file, 'a') as logs:
		logs.write(capture + "\n")
	
	
if __name__== "__main__":
	# Passes parameters set by user over to the fetch_atg() function, saves output as capture.
	capture = fetch_atg(ip, port, command, tank)

	# Logs the data we just collected to the user-defined log file.
	report_txt(log_file, capture)
