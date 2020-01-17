#this is not goto LABEL113 will not be able to execute LABEL200 with code flow

class LABEL113:
	@staticmethod
	def execute():
		print("IM 113")
	pass

class LABEL200:
	@staticmethod
	def execute():
		print("IM 200")
	pass

try:
	print("started EXECUTING")
	if 1 == 1:
		raise LABEL113 #goto 113
	elif 1 == 1:
		raise LABEL200 #goto 200

except LABEL113:
	print("started EXECUTING 113")
	LABEL113.execute()

except LABEL200:
	print("started EXECUTING 200")
	LABEL200.execute()

finally:
	LABEL200.execute()
	print("FINALLY")


try:
	raise Exception("hello")
except Exception as msg:
	print(msg)
