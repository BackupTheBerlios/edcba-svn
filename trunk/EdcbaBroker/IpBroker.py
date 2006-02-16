#!/usr/bin/env python

# This is a IP (L3) Broker for the Linux "ip addr" command
# Copyright 2006 John T. Kamenik, GLPL, All rights reserved.

import sys, signal
from ControlBroker import ControlBroker
from pprint import pprint

try:
	from omniORB import CORBA
	import omniORB

	omniORB.omniidlArguments(["-I./idl"])
	omniORB.importIDL("./idl/BrokerNameService.idl")
	omniORB.importIDL("./idl/IPControlBroker.idl")

	import EDCBA__POA
	import EDCBA

	pprint( EDCBA__POA.__dict__ )
	pprint( EDCBA.__dict__ )

	base  = EDCBA__POA.IPControlBroker
except object,reason:
	print "Exception",reason
	base  = object


class MyInterface(EDCBA.IPInterface):
	def __init__(self):
		EDCBA.IPInterface.__init__(self,None,None,None,None,None)


class IPBroker(base,ControlBroker):
	def __init__(self,orb):
		ControlBroker.__init__(self,orb,"IP Broker")
		self.ips = {}

	def addInterface(self,name):
		print "Adding: %s" % name
		if name in self.ips:
			print "%s already exists" % name
			return False
		self.ips[name] = MyInterface()
		self.ips[name].name = name
		return True

	def editInterface(self,name,ip,mask,broadcast):
		if not name or name not in self.ips:
			return False
		if ip:
			self.ips[name].ip = ip
		if mask:
			self.ips[name].mask = mask
		if broadcast:
			self.ips[name].broadcast = broadcast

	def bindInterface(self,name,l2):
		pass

	def unbindInterface(self,name):
		pass

	def getInterface(self,name):
		try:
			print self.ips[name]
			return self.ips[name]._narrow(EDCBA.IPInterface)
		except KeyError:
			None

	def getInterfaces(self):
		return self.ips.values()

	def getStatus(self):
		pass

	def test(self,test):
		print test


def quitHandler(signum, frame):
	raise KeyboardInterrupt


if __name__ == "__main__":
	orb = CORBA.ORB_init(sys.argv)

	obj = IPBroker(orb)

	poa = orb.resolve_initial_references("RootPOA")
	poaManager = poa._get_the_POAManager()
	poaManager.activate()

	signal.signal(signal.SIGQUIT, quitHandler)
	signal.signal(signal.SIGTSTP, quitHandler)
	signal.signal(signal.SIGINT,  quitHandler)

	try:
		signal.pause()
	except KeyboardInterrupt:
		pass

	obj.deregister()
