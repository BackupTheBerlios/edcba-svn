#!/usr/bin/env python

# Copyright 2004 W. Borgert, GNU General Public License

# This test code is chaotic, because it combines CORBA client and
# server, both with variants for four different Python ORBs, one of
# which doesn't even support the POA.  Never ever do such thing in
# real-world applications!

import os, socket, sys, signal
from EdcbaBroker.ControlBroker import ControlBroker

try:
	from omniORB import CORBA
	import omniORB

	# for now assume we are being run from edcba root
	omniORB.omniidlArguments(["-I./idl"])
	omniORB.importIDL("./idl/BrokerNameService.idl")
	omniORB.importIDL("./idl/echo.idl")
	
	import EDCBA__POA as EDCBA
except:
	print "Failed to initialise CORBA"
	

def quitHandler(signum, frame):
	print "\nStopping Echo Client"
	raise KeyboardInterrupt

if __name__ == '__main__':
	print "Starting Echo Client"
	orb = CORBA.ORB_init(sys.argv)
	# client code
	ns_ior = file('/tmp/BrokerNameService.ior').read()
	ns_obj = orb.string_to_object(ns_ior)
	ns  = ns_obj._narrow(EDCBA.BrokerNameService)

	echo_ior = ns.getAddressOf("Echo Server")
	print "IOR: %s" % (echo_ior)
	echo_obj = orb.string_to_object(echo_ior)
	print "OBJ: %s" % (echo_obj)
	echo  = echo_obj._narrow(EDCBA.Echo)
	print "REL: %s" % (echo)
	
	signal.signal(signal.SIGQUIT, quitHandler)
	signal.signal(signal.SIGTSTP, quitHandler)
	signal.signal(signal.SIGINT,  quitHandler)

	#print echo.do_echo("Hello!")
	try:
		while True:
			try: s = raw_input("> ")
			except EOFError: s = 'EOF'
			echo.do_echo(s)
			if s == 'EOF': break
	except KeyboardInterrupt: pass


