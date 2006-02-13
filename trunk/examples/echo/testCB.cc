
#include <ControlBroker.hh>
#include <ControlBroker.hpp>
#include <echo.hh>
#include <iostream>
#include <signal.h>
#include <pthread.h>

class Echo_i : public POA_EDCBA::Echo, public ControlBroker,
	       public PortableServer::RefCountServantBase
{
public:
	inline Echo_i(CORBA::ORB_ptr orb) : ControlBroker::ControlBroker(orb, "Echo Server") {}
	virtual char* do_echo(const char* mesg);
};

char* Echo_i::do_echo(const char* mesg)
{
  std::cerr << "Upcall " << mesg << std::endl;
  return CORBA::string_dup(mesg);
}

Echo_i *servant = NULL;
CORBA::ORB_var orb;

/* Signal handler for SIGINT. */
void SIGINT_handler (int signum)
{
  assert (signum == SIGINT);
  std::cerr << "Caught SIGINT" << std::endl;
	//pman->deactivate();
	servant->deregister();
	orb->shutdown(0);
}

/* Signal handler for SIGQUIT. */
void SIGQUIT_handler (int signum)
{
  assert (signum == SIGQUIT);
  std::cerr << "Caught SIGQUIT" << std::endl;
}

int main(int argc, char** argv)
{
	struct sigaction sa;
	sigemptyset (&sa.sa_mask);
	sa.sa_flags = 0;
	
	/* Register the handler for SIGINT. */
	sa.sa_handler = SIGINT_handler;
	sigaction (SIGINT, &sa, 0);
	
	/* Register the handler for SIGQUIT. */
	sa.sa_handler =  SIGQUIT_handler;
	sigaction (SIGQUIT, &sa, 0);
	
	
  try {
    orb = CORBA::ORB_init(argc, argv);

    CORBA::Object_var obj = orb->resolve_initial_references("RootPOA");
    PortableServer::POA_var poa = PortableServer::POA::_narrow(obj);

    servant = new Echo_i(orb);
      
    PortableServer::ObjectId_var myechoid = poa->activate_object(servant);
		
		servant->nsregister();


    servant->_remove_ref();

    PortableServer::POAManager_var pman = poa->the_POAManager();
    pman->activate();

    orb->run();
		std::cout << "Stopping..." << std::endl;
		//orb->destroy();
	  //delete servant;
  }
  catch(CORBA::SystemException&) {
    std::cerr << "Caught CORBA::SystemException." << std::endl;
  }
  catch(CORBA::Exception&) {
    std::cerr << "Caught CORBA::Exception." << std::endl;
  }
  catch(omniORB::fatalException& fe) {
    std::cerr << "Caught omniORB::fatalException:" << std::endl;
    std::cerr << "  file: " << fe.file() << std::endl;
    std::cerr << "  line: " << fe.line() << std::endl;
    std::cerr << "  mesg: " << fe.errmsg() << std::endl;
  }
  catch(...) {
    std::cerr << "Caught unknown exception." << std::endl;
  }

  return 0;
}
