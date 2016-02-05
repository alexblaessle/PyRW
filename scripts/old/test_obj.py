class animal:
	def __init__(self,name):
		self.name=name
	
	def sayHi(self):
		print "Hi"
	
class dog(animal):
	def __init__(self,onleash,name):
		self.onleash=onleash
		animal.__init__(self,name)

d=dog("yes","doggy")

print d
d.sayHi()
print d.name