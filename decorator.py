#decorator without param
def mydec(f):
    def _inner():
        print("dec call")
        return f();
    return _inner

@mydec
def mycall():
    print("actual call")
    return True



#decorator with param using functions
#def tag(*args):
#    t=args[0]
#    def _gettag(f):
#        def _tag(*args,**kwargs):
#            print("<"+t+">");
#            r=f(''.join(args))
#            print("</"+t+">")
#            return r
#        return _tag
#    return _gettag

#decorator with param using class
class tag:
    def __init__(self,tag):
        self.tag = tag ;

    def __call__(self,f):
        from functools import wraps
        @wraps(f)
        def _tag(*args,**kwargs):
            print("<"+self.tag+">");
            r=f(''.join(args))
            print("</"+self.tag+">")
            return r
        return _tag

@tag("a")
def mycall2(content):
    "do some print"
    print(content)
    return True

#print(mycall())
print(mycall2("HTML","HTML5"))


print(mycall2.__name__)  # prints 'f'
print(mycall2.__doc__)   # prints 'does some print'


print("==========================")

def getFuncName(f):
    from functools import wraps
    @wraps(f)
    def __get_func_name(*args,**kwargs):
        f(*args,__name__=f.__name__,**kwargs)
    return __get_func_name
    

@getFuncName
def hello_my_func(x,y,z,key,__name__):
    print("hello_my_func>>>")
    print(__name__)
    print(key)
    print("{}{}{}".format(x,y,z))


hello_my_func(1,2,3,key="key")
