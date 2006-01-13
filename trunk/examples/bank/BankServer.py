from omniORB import CORBA
import omniORB
import sys

omniORB.importIDL('./Bank.idl')

class base: pass

try:
	import Bank__POA
	base = Bank__POA.Account
except: pass


class Account(base):
	def __init__(self, bal):
		self.balance = bal;
		print self.__dict__, self
		
	def deposit(self, amount):
		print "Adding %s to %s"%(amount, self.balance)
		self.balance += amount
		
	def notice(self, text):
		print "NOTICE: %s"%(text)
		
	def withdraw(self, amount):
		print self.__dict__, self
		if self.balance - amount < 0:
			d = Bank__POA.Account.InsuffientFunds()
			d.overdraft = amount - self.balance
			raise Bank__POA.Account.InsufficientFunds, d
		else:
			self.balance = self.balance - amount
			
	def getBalance(self):
		print "Balance is %s" %(self.balance)
		return self.balance


if __name__ == '__main__':
	orb = CORBA.ORB_init(sys.argv)
	ref = Account(20)._this()
	print ref
	print orb.list_initial_services()
	
	open("/tmp/bank_example.ior","w").write(orb.object_to_string(ref))
	
	poa = orb.resolve_initial_references("RootPOA")
	
	poa._get_the_POAManager().activate()
	orb.run()
