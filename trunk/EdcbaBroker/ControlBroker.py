#!/usr/bin/env python

# The basic ControlBroker from which all others flow.
# Copyright 2006 John T. Kamenik, LGPL, All rights reserved.

import os, sys

try:
	from omniORB import CORBA
	import omniORB

	# for now assume we are being run from edcba root
	omniORB.importIDL("./idl/ControlBroker.idl")
	omniORB.importIDL("./idl/BrokerNameService.idl")

	import EDCBA__POA as EDCBA

	base = EDCBA.ControlBroker
except:
	# if we can't be a CORBA object, then we can't be anything
	base = object


class ControlBroker(base):
	def __init__(self, orb, name="Control Broker"):
		'''Creates a generic Control Broker'''
		self.name = name
		self.orb  = orb
		self.auth = None
		self.register()

	def __del__(self):
		'''Called when this class is cleaned up'''
		print "Deleting %s" % (self.name)
		try:
			if self.auth:
				ns.deregister(self.auth,self.name)
		except: pass

	def register(self):
		'''Registers with the BrokerNameService'''
		ior = file('/tmp/BrokerNameService.ior').read()
		obj = self.orb.string_to_object(ior)
		ns  = obj._narrow(EDCBA.BrokerNameService)
		auth = ns.nsregister(self.name,self.orb.object_to_string(self._this()))
		if auth:
			self.auth = auth
			self.ns   = ns
			return True
		else:
			return False

	def deregister(self):
		if self.auth is not None:
			if self.ns.deregister(self.auth,self.name):
				self.auth = None
				self.ns   = None
				return True
			else:
				print "Unable to deregister"
				return False
		else:
			return False

	def isRegistered(self):
		return self.auth is not None

	def getName(self):
		return self.name

	def serialize(self, auth, profile):
		pass

	def deserialize(self, auth, profile):
		pass


if __name__ == "__main__":
	orb = CORBA.ORB_init(sys.argv)

	obj = ControlBroker(orb)
	obj.deregister()
