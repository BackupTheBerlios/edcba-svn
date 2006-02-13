
#include <omniORB4/CORBA.h>
#include <BrokerNameService.hh>
#include <ControlBroker.hh>
#include <string>


class ControlBroker : public POA_EDCBA::ControlBroker {
	public:
		ControlBroker(CORBA::ORB_ptr orb, char *name = "Control Broker");
		~ControlBroker();
			
		bool nsregister();
				
		bool deregister();
				
		bool isRegistered();
			
		// Interface Functions
		virtual char* getName();
		virtual void serialize(const char *auth, const char *profile);
		virtual void deserialize(const char *auth, const char *profile);
	
	private:
		std::string m_auth;
		std::string m_name;
		CORBA::ORB_ptr m_orb;
		EDCBA::BrokerNameService_ptr m_nameServer;
};
