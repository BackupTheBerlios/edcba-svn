#!/usr/bin/env python

# Copyright 2004 W. Borgert, GNU General Public License

# This test code is chaotic, because it combines CORBA client and
# server, both with variants for four different Python ORBs, one of
# which doesn't even support the POA.  Never ever do such thing in
# real-world applications!

import os, socket, sys

SERVER = True


file('echo.idl', 'w').write("""
module Test {
    interface Echo {
        string do_echo(in string message);
        void quit();
    };
};
""")

# For omniOrb
from omniORB import CORBA

# For ORBitPy
#import CORBA

# For pyORBit
#from ORBit import CORBA


try:
    if CORBA.ORB_ID == "omniORB4":
        import omniORB
        omniORB.importIDL("./echo.idl")
        print "using omniORB"
    elif CORBA.ORB_ID == "orbit-local-orb":
        print "using ORBitPy" # magically takes '*.idl' from cwd!
    else:
        print "using unknown ORB"
except AttributeError: # pyORBit's CORBA has no ORB_ID
    import ORBit
    ORBit.load_file("./echo.idl")
    print "using pyORBit"

# Import the IDL Stuff
try:
		import Test__POA
		base = Test__POA.Echo
except: pass

class EchoServant(base):
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
	
	servant = EchoServant()
	objref = servant._this()
	file('iorfile', 'w').write(orb.object_to_string(objref))
	poa = orb.resolve_initial_references("RootPOA")
	poaManager = poa._get_the_POAManager() 
	poaManager.activate()
	orb.run()
	os.unlink("iorfile")
	os.unlink("echo.idl")

