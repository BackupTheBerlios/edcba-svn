import CORBA, omniORB
import sys

omniORB.importIDL('./Bank.idl')

import Bank
class base: pass

orb = CORBA.ORB_init(sys.argv)

ior = open("/tmp/bank_example.ior").read()
obj = orb.string_to_object(ior)
account = obj._narrow(Bank.Account)

print account

account.notice( "Getting current balance" )
print "Current balance: %i" %(account.getBalance())
try:
	account.notice( "Withdrawing 30" )
	account.withdraw(30)
	print "New balance: %i" %(account.getBalance())
except Bank.Account.InsufficientFunds, data:
	print "Overdrawn: %i"%(data.overdraft)
