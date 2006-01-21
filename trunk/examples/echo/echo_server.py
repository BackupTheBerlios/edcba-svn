#!/usr/bin/env python

# Copyright 2004 W. Borgert, GNU General Public License

# This test code is chaotic, because it combines CORBA client and
# server, both with variants for four different Python ORBs, one of
# which doesn't even support the POA.  Never ever do such thing in
# real-world applications!

import os, socket, sys
from EdcbaBroker.ControlBroker import ControlBroker

try:
	from omniORB import CORBA
	import omniORB
	
	# for now assume we are being run from edcba root
	omniORB.importIDL("./idl/BrokerNameService.idl")
	omniORB.importIDL("./examples/echo/echo.idl")
	
	import EDCBA__POA as EDCBA
	
	base = EDCBA.Echo
except:
	# if we can't be a CORBA object, then we can't be anything
	base = object

# The echo servant class inherits from the ControlBroker class to get the 
#  Name Server registration functions
class EchoServant(ControlBroker,base):
	def __init__(self, orb):
		ControlBroker.__init__(self, orb, "Echo Server")

	def do_echo(self, message):
		print "Got: '%s'" % message
		return ""
	def quit(self):
		print "Good-bye!"
		global orb
		orb.shutdown(0)

if __name__ == '__main__':
	#del sys.argv[1:3] # pyORBit doesn't like some arguments
	orb = CORBA.ORB_init(sys.argv)
	
	servant = EchoServant(orb)
	
	#pprint(sys.modules['EDCBA'].__dict__)

	#poa = orb.resolve_initial_references("RootPOA")
	#poaManager = poa._get_the_POAManager() 
	#poaManager.activate()
	servant.deregister()
	orb.run()

