#!/usr/bin/env python

# This is a IP (L3) Broker
# Copyright 2006 John T. Kamenik, GLPL, All rights reserved.

import sys
from ControlBroker import ControlBroker
from pprint import pprint

try:
	from omniORB import CORBA
	import omniORB
	
	omniORB.omniidlArguments(["-I./idl"])
	omniORB.importIDL("./idl/BrokerNameService.idl")
	omniORB.importIDL("./idl/IPControlBroker.idl")
	
	import EDCBA__POA as EDCBA
	
	base  = EDCBA.IPControlBroker
except:
	print "loading exception"
	base  = object
	ibase = object
	
#pprint( sys.modules["EDCBA"].__dict__ )
	

class IPBroker(base,ControlBroker):
	def __init__(self,orb):
		super(IPBroker, self).__init__(self,orb,"IP Broker")
		self.ips = {}
		
	def addInterface(self,name):
		if name in self.ips:
			return False
		self.ips[name] = EDCBA.IPInterface(name)
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
		
	def getInterfaces(self):
		pass
		
	def getStatus(self):
		pass
		
if __name__ == "__main__":
	orb = CORBA.ORB_init(sys.argv)
	
	obj = IPBroker(orb)
	
	print obj.__dict__
	
	obj.deregister()
