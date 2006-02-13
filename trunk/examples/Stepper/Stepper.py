#!/usr/bin/env python

# Stepper .
# Copyright 2006 John T. Kamenik, GLPL, All rights reserved.

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

	base = EDCBA.Stepper
except:
	# if we can't be a CORBA object, then we can't be anything
	base = object


# The echo servant class inherits from the ControlBroker class to get the
#  Name Server registration functions
class StepperServant(base,ControlBroker):
	def __init__(self, orb):
		print self.__dict__
		print self._this()
		ControlBroker.__init__(self, orb, "Stepper")
		print "Starting Stepper Server"
		self.base       = 0
		self.stepTaken  = 0
		self.stepAmount = 1

	def setBase(self, base):
		self.base = base

	def setStep(self, step):
		self.stepAmount = step

	def reset(self):
		self.stepTaken = 0

	def next(self):
		self.stepTaken += self.stepAmount
		return self.base + self.stepTaken


def quitHandler(signum, frame):
	print "Stopping Echo Server"
	raise KeyboardInterrupt

if __name__ == '__main__':
	orb = CORBA.ORB_init(sys.argv)

	servant = StepperServant(orb)

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
