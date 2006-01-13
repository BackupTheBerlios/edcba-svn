#!/usr/bin/env python

# Copyright 2004 W. Borgert, GNU General Public License

# This test code is chaotic, because it combines CORBA client and
# server, both with variants for four different Python ORBs, one of
# which doesn't even support the POA.  Never ever do such thing in
# real-world applications!

import os, socket, sys

# For Fnorb
#from Fnorb.orb import CORBA

# For omniOrb
from omniORB import CORBA

# For ORBitPy
#import CORBA

# For pyORBit
#from ORBit import CORBA


try:
    if CORBA.ORB_ID == "The ORB called Fnorb v1.1.Return.of.Fnorb":
        os.system("fnidl echo.idl")
        print "using Fnorb"
    elif CORBA.ORB_ID == "omniORB4":
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

#Import the IDL
import Test
class base: pass

if __name__ == '__main__':
	#del sys.argv[1:3] # pyORBit doesn't like some arguments
	orb = CORBA.ORB_init(sys.argv)
	# client code
	ior = file('iorfile').read()
	obj = orb.string_to_object(ior)
	echo = obj._narrow(Test.Echo)
	#print echo.do_echo("Hello!")
	while True:
		try: s = raw_input("> ")
		except EOFError: s = 'EOF'
		echo.do_echo(s)
		if s == 'EOF': break
	
	try: # as we kill the server, an exception may occur
		echo.quit()
	except CORBA.COMM_FAILURE:
		print "pyORBit -o )- pyORBit or Fnorb -o )- any ORB?"
	except CORBA.TRANSIENT:
		print "pyORBit -o )- omniORB?"
	except socket.error:
		print "pyORBit -o )- Fnorb?"


