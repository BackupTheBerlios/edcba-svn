// eg2_clt.cc - This is the source code of example 2 used in Chapter 2
//              "The Basics" of the omniORB user guide.
//
//              This is the client. The object reference is given as a
//              stringified IOR on the command line.
//
// Usage: eg2_clt <object reference>
//

#include <echo.hh>

#ifdef HAVE_STD
#  include <iostream>
#  include <fstream>
   using namespace std;
#else
#  include <iostream.h>
#  include <fstream.h>
#endif


static void hello(EDCBA::Echo_ptr e)
{
  CORBA::String_var src = (const char*) "Hello!";

  CORBA::String_var dest = e->do_echo(src);

  cerr << "I said, \"" << (char*)src << "\"." << endl
       << "The Echo object replied, \"" << (char*)dest <<"\"." << endl;
}

//////////////////////////////////////////////////////////////////////

int main(int argc, char** argv)
{


  try {
    CORBA::ORB_var orb = CORBA::ORB_init(argc, argv);
                                                         
    //if( argc != 2 ) {
    //  cerr << "usage:  eg2_clt <object reference>" << endl;
    //  return 1;
    //}
		
		ifstream file;
		file.open("echo.ior");
		char buffer[500];
		file >> (char*)buffer;

    CORBA::Object_var obj = orb->string_to_object(buffer);
    EDCBA::Echo_var echoref = EDCBA::Echo::_narrow(obj);
    if( CORBA::is_nil(echoref) ) {
      cerr << "Can't narrow reference to type Echo (or it was nil)." << endl;
      return 1;
    }
    for (CORBA::ULong count=0; count<10; count++) 
      hello(echoref);

    orb->destroy();
  }
  catch(CORBA::COMM_FAILURE& ex) {
    cerr << "Caught system exception COMM_FAILURE -- unable to contact the "
         << "object." << endl;
  }
  catch(CORBA::SystemException&) {
    cerr << "Caught a CORBA::SystemException." << endl;
  }
  catch(CORBA::Exception&) {
    cerr << "Caught CORBA::Exception." << endl;
  }
  catch(omniORB::fatalException& fe) {
    cerr << "Caught omniORB::fatalException:" << endl;
    cerr << "  file: " << fe.file() << endl;
    cerr << "  line: " << fe.line() << endl;
    cerr << "  mesg: " << fe.errmsg() << endl;
  }
  catch(...) {
    cerr << "Caught unknown exception." << endl;
  }
  return 0;
}
