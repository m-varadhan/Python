import weakref

class IdentityWrapperWithInvalidKeyObject(object):
	def __init__(self):
		self._data = {}

	def __getitem__(self, obj):
		val = self._data[id(obj)]
		return val

	def __setitem__(self, obj, value):
		key = id(obj)
		self._data[key] = value

	def __delitem__(self, obj):
		del self._data[id(obj)]

	def count(self):
		return (len(self._data))

class IdentityWrapperCleanInvalidKeyObject(object):
	def __init__(self):
		self._data = {}

	def __getitem__(self, obj):
		_, val = self._data[id(obj)]
		return val

	def __setitem__(self, obj, value):
		key = id(obj)
		try:
			ref, _ = self._data[key]
		except KeyError:
			def on_destroy(_):
				print("removed from good dict")
				del self._data[key]
			ref = weakref.ref(obj, on_destroy)
		self._data[key] = ref, value

	def __delitem__(self, obj):
		del self._data[id(obj)]

	def count(self):
		return (len(self._data))

class Bar:
	pass

class Foo:
	pass

myObjDict_bad = IdentityWrapperWithInvalidKeyObject()
myObjDict_good = IdentityWrapperCleanInvalidKeyObject()
	

def myfunc():
	bar = Bar()
	myObjDict_bad[bar] = "My Bar"
	myObjDict_good[bar] = "My Bar"
	print(f"bad count {myObjDict_bad.count()}")
	print(f"good count {myObjDict_good.count()}")


foo = Foo()
myObjDict_bad[foo] = "My Foo"
myObjDict_good[foo] = "My Foo"
myfunc()

print(f"bad count {myObjDict_bad.count()}")
print(f"good count {myObjDict_good.count()}")
