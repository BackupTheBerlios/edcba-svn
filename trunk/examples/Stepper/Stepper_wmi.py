#!/usr/bin/env python

print "content-type: text/html"

#print header
print "<html><body>"

import sys

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


orb = CORBA.ORB_init(sys.argv)
ns_ior = file('/tmp/BrokerNameService.ior').read()
ns_obj = orb.string_to_object(ns_ior)
ns  = ns_obj._narrow(EDCBA.BrokerNameService)

stepper_ior = ns.getAddressOf("Stepper")
stepper_obj = orb.string_to_object(stepper_ior)
stepper     = stepper_obj._narrow(EDCBA.Stepper)

size = 10

print '<table border="1">'
for row in xrange(0,size):
	print '<th colspan="',size,'">Step of ',row+1,'</th>'
	print "<tr>"
	stepper.setStep(row+1)
	for col in xrange(0,size):
		print "<td>"
		print stepper.next()
		print "</td>"
	print "</tr>"
print "</table><br>"

print '<table border="1">'
stepper.setStep(col+1)
for step in xrange(0,size):
	print '<th>Step of ',step+1,'</th>'
for row in xrange(0,size):
	print "<tr>"
	for col in xrange(0,size):
		print "<td>"
		print stepper.next(),
		print '+ ',col+1,' ='
		print "</td>"
		stepper.setStep(col+1)
	print "</tr>"
print "</table>"
