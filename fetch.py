import telnetlib
def fetch(ip, port):
	tn = telnetlib.Telnet(ip, port) 
	tn.write('\x01I20100')
	tn.read_until('20100')
	open("tankreading.txt","a").write(tn.read_until('\x03',10).replace("\x03",""))
	tn.close()
	
fetch(raw_input("What is the IP address? \n\n"), 10001)
