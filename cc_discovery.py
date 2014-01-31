#!/usr/bin/python
import select
import sys
import socket
import re

#http://www.dial-multiscreen.org/dial-protocol-specification
#M-SEARCH * HTTP/1.1
#HOST: 239.255.255.250:1900
#MAN: "ssdp:discover"
#MX: seconds to delay response
#ST: urn:dial-multiscreen-org:service:dial:1
#USER-AGENT: OS/version product/version

SSDP_ADDR = "239.255.255.250";
SSDP_PORT = 1900;
SSDP_MX = 1;
SSDP_ST = "urn:dial-multiscreen-org:service:dial:1";

ssdpRequest = "M-SEARCH * HTTP/1.1\r\n" + \
                "HOST: %s:%d\r\n" % (SSDP_ADDR, SSDP_PORT) + \
                "MAN: \"ssdp:discover\"\r\n" + \
                "MX: %d\r\n" % (SSDP_MX, ) + \
                "ST: %s\r\n" % (SSDP_ST, ) + "\r\n";

try:
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error, msg:
	sys.stderr.write("[ERROR] %s\n" % msg[1])
	s.close()
	sys.exit(1)

sock.sendto(ssdpRequest, (SSDP_ADDR, SSDP_PORT))
sock.setblocking(0)
ready = select.select([sock], [], [], 10)
if ready[0]:
	data = sock.recv(4096)
#	print 'Received', repr(data)
	tests = data.split("\r\n")
	print tests
	for test in tests:
		if test.startswith("LOCATION") and test.endswith("/ssdp/device-desc.xml"):
			url= test.strip("LOCATION: ")
			ip = re.findall( r'[0-9]+(?:\.[0-9]+){3}', url )
			print ip

	
else:
	print "No ChromeCast Dial Device found"

