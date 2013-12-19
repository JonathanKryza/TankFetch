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
def fetch(ip, port):
	tn = telnetlib.Telnet(ip, port) 
	tn.write('\x01I20100')
	tn.read_until('20100')
	open("tankreading.txt","a").write(tn.read_until('\x03',10).replace("\x03",""))
	tn.close()
	
fetch(raw_input("What is the IP address? \n\n"), 10001)
