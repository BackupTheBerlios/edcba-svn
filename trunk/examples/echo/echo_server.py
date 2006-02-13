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

	base = EDCBA.Echo
except:
	# if we can't be a CORBA object, then we can't be anything
	base = object
	print "Failed to Initialize CORBA"

# The echo servant class inherits from the ControlBroker class to get the
#  Name Server registration functions
class EchoServant(base,ControlBroker):
	def __init__(self, orb):
		ControlBroker.__init__(self, orb, "Echo Server")
		print "Starting Echo Sterver"

	def do_echo(self, message):
		print "Got: '%s'" % message
		return message


def quitHandler(signum, frame):
	print "Stopping Echo Server"
	raise KeyboardInterrupt

if __name__ == '__main__':
	orb = CORBA.ORB_init(sys.argv)

	servant = EchoServant(orb)
	
	poa = orb.resolve_initial_references("RootPOA")
	poaManager = poa._get_the_POAManager() 
	poaManager.activate()

	signal.signal(signal.SIGQUIT, quitHandler)
	signal.signal(signal.SIGTSTP, quitHandler)
	signal.signal(signal.SIGINT,  quitHandler)

	try:
		#orb.run()
		signal.pause()
	except KeyboardInterrupt: pass

	servant.deregister()
