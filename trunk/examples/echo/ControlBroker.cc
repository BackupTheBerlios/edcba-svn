
#include <iostream>
#include <fstream>
#include <ControlBroker.hh>
#include <ControlBroker.hpp>


ControlBroker::ControlBroker(CORBA::ORB_ptr orb, char *name) {
	m_orb = orb;
	m_name = name;
	m_nameServer = EDCBA::BrokerNameService::_nil();
}

ControlBroker::~ControlBroker() {
	//deregister();
}

// Registers with the BrokerNameService
bool ControlBroker::nsregister() {
	std::ifstream file;
	char buffer[500];
	
	// Find the name service
	file.open("/tmp/BrokerNameService.ior");
	file >> (char*)buffer;
	
	CORBA::Object_var obj = m_orb->string_to_object(buffer);
	m_nameServer = EDCBA::BrokerNameService::_narrow(obj);
	if( CORBA::is_nil(m_nameServer) ) {
		std::cerr << "Can't narrow reference to type BrokerNameService (or it was nil)." << std::endl;
		return 1;
	}
	
	// Register with the name service
	obj = _this();
  CORBA::String_var sior(m_orb->object_to_string(obj));
	//CORBA::String_var name((const char *)m_name.c_str());
	std::string auth = m_nameServer->nsregister(m_name.c_str(), m_orb->object_to_string(obj));
		
	if (auth != "") {
		m_auth = auth;
		return true;
	}
	m_nameServer = EDCBA::BrokerNameService::_nil();
	return false;
}
			
bool ControlBroker::deregister() {
	if (m_auth != "") {
		if (m_nameServer->deregister(m_auth.c_str(),m_name.c_str())) {
			m_auth = "";
			m_nameServer = EDCBA::BrokerNameService::_nil();
			return true;
		} else {
			std::cerr << "Unable to deregister" << std::endl;
			return false;
		}
	}
	return false;
}
			
bool ControlBroker::isRegistered() {
	return m_auth != "";
}
		
char* ControlBroker::getName() {
	return (char*)m_name.c_str();
}
		
void ControlBroker::serialize(const char *auth, const char *profile) {
}
	
void ControlBroker::deserialize(const char *auth, const char *profile) {
}
