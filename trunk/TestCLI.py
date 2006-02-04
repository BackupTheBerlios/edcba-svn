#!/usr/bin/env python

# A simple test cli.
# Copyright 2006 John T. Kamenik, GLPL, All rights reserved.

import sys

from omniORB import CORBA
import omniORB

omniORB.importIDL("./idl/BrokerNameService.idl")

import EDCBA__POA as EDCBA

# for now assume we are being run from edcba root
omniORB.importIDL("./idl/BrokerNameService.idl")

orb          = CORBA.ORB_init(sys.argv)
ior          = file('/tmp/BrokerNameService.ior').read()
obj          = orb.string_to_object(ior)
nameservice  = obj._narrow(EDCBA.BrokerNameService)

registered = nameservice.getRegistered()

for item in registered:
	print "%s: %s" %( item, nameservice.getAddressOf(item))
