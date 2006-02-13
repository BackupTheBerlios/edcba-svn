echoidlstub   = echoSK.cc
echoidlheader = echo.hh
echoidlfile   = ../../idl/echo.idl

.PHONY: all clean $(echoidlstub) cleanecho echo controlbroker cleancontrolbroker

all: controlbroker

clean: cleanecho cleancontrolbroker cleanns



echo: $(echoidlstub) echoclient echoserver

echoclient: eg2_clt.cc
	g++ -I. -o echoc eg2_clt.cc $(echoidlstub) -lomniORB4 -lomnithread
	
echoserver: eg2_impl.cc
	g++ -I. -o echod eg2_impl.cc $(echoidlstub) -lomniORB4 -lomnithread

$(echoidlstub): $(echoidlfile)
	omniidl -I../../idl -bcxx $(echoidlfile)

cleanecho:
	rm -rf $(echoidlstub) $(echoidlheader) echoc echod
	
cbidlstub   = ControlBrokerSK.cc
cbidlheader = ControlBroker.hh
cbidlfile   = ../../idl/ControlBroker.idl

nsidlstub   = BrokerNameServiceSK.cc
nsidlheader = BrokerNameService.hh
nsidlfile   = ../../idl/BrokerNameService.idl

controlbroker: $(cbidlstub) $(nsidlstub) $(echoidlstub) ControlBroker.cc testCB.cc
	g++ -I. -o controlbroker ControlBroker.cc testCB.cc $(cbidlstub) $(nsidlstub) $(echoidlstub) -lomniORB4 -lomnithread
	
	
$(cbidlstub): $(cbidlfile)
	omniidl -bcxx $(cbidlfile)
	
$(nsidlstub): $(nsidlfile)
	omniidl -bcxx $(nsidlfile)

cleancontrolbroker:
	rm -rf $(cbidlstub) $(cbidlheader) controlbroker
	
cleanns:
	rm -rf $(nsidlstub) $(nsidlheader) controlbroker