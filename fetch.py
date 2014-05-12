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
import sys
import datetime

ip = ''                        #The IP address of the ATG you are polling. Must be in quotations.
port =                         #The default for most is 10001
command = 'i201'               #Lowercase 'i' is used for the hexadecimal format. Uppercase 'I' for a human readable output.
command2 = 'I202'              #Go to the docs folder for a full listing of commands or visit https://www.veeder.com
tank = '00'                    #'00' means ALL. For a specific tank, enter as follows: Tank 1 = "01", Tank 12 = "12", etc

def fetch_tcpip():
	tn = telnetlib.Telnet(ip, port)
	tn.write('\x01' + str(command) + str(tank))
	tn.read_until(str(command) + str(tank))
	global capture1
	capture1 = tn.read_until('\x03',10).replace('\x03','')
	tn.write('\x01' + str(command2) + str(tank))
	tn.read_until(str(command2) + str(tank))
	global capture2
	capture2 = tn.read_until('\x03',10).replace('\x03','')
	tn.close()
	

def report_txt():                               #Creating a simple txt file out of the output
	now = datetime.datetime.now()
        date = now.strftime('%m-%d-%Y')         #Date format - visit https://docs.python.org/2/library/datetime.html
        #Below is an example. State the directory and name of the file. 
	open('\user\directory\\' + 'filename' + date + '.txt', 'w').write(capture2)  #.write can be anything you capture or you can combine multiples. Ex. .wrint(capture1 + capture2)
	
	
if __name__=="__main__":
	fetch_tcpip()
	report_txt()
