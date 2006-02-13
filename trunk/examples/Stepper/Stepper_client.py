#!/usr/bin/env python


import os, socket, sys, signal
from EdcbaBroker.ControlBroker import ControlBroker

try:
	from omniORB import CORBA
	import omniORB

	# for now assume we are being run from edcba root
	omniORB.omniidlArguments(["-I./idl"])
	omniORB.importIDL("./idl/BrokerNameService.idl")
	omniORB.importIDL("./idl/Stepper.idl")

	import EDCBA__POA as EDCBA
except:
	print "Failed to initialise CORBA"


def quitHandler(signum, frame):
	print "\nStopping Stepper Client"
	raise KeyboardInterrupt

if __name__ == '__main__':
	print "Starting Stepper Client"
	orb = CORBA.ORB_init(sys.argv)
	# client code
	ns_ior = file('/tmp/BrokerNameService.ior').read()
	ns_obj = orb.string_to_object(ns_ior)
	ns  = ns_obj._narrow(EDCBA.BrokerNameService)

	stepper_ior = ns.getAddressOf("Stepper")
	print "IOR: %s" % (stepper_ior)
	stepper_obj = orb.string_to_object(stepper_ior)
	print "OBJ: %s" % (stepper_obj)
	stepper     = stepper_obj._narrow(EDCBA.Stepper)
	print "REL: %s" % (stepper)

	signal.signal(signal.SIGQUIT, quitHandler)
	signal.signal(signal.SIGTSTP, quitHandler)
	signal.signal(signal.SIGINT,  quitHandler)

	for i in xrange(0,100):
		print stepper.next()

	stepper.setBase(100)
	stepper.setStep(2)
	stepper.reset()
	for i in xrange(0,50):
		print stepper.next()

