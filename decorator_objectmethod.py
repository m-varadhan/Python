import traceback
import logging
import sys

import functools

class tag:
    def __init__(self,tag):
        self.tag = tag ;

    def __call__(self,f,*args,**kargs):
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

print("==========================")


class mydeco(object):
    def __init__(self,func,*args,**kargs):
        print("Called init")
        self.func = func
        print(func)
        print(args)
        print(kargs)
        print("Called init")

    def __get__(self, obj, objname):
        print("Called get")
        if obj is None:
            return self
        print(str(obj))
        print(objname)
        print("Called get")
        return functools.partial(self.__call__,obj)

    def __call__(self,*args,**kargs):
        print("Called call")
        print(str(self))
        print(args)
        print(kargs)
        print("Called call")
        self.func(*args,**kargs)

class mydeco2(object):
    def __init__(self,delete=True,*args,**kargs):
        print("Called call init mydeco2")
        self.delete = delete

    #def __get__(self, obj, owner):
    #    return functools.partial(self.__call__,obj)

    def __call__(self,func):
        print("Called call of mydeco2")
        #print(str(self))
        #print(str(func))
        #print(args)
        #print(kargs)
        #func(*args,**kargs)
        def newfunc(self,*fargs,**fkargs):
            print("Called call of mydeco2: newfunc")
            #print(args)
            #print(kargs)
            print(fargs)
            print(fkargs)
            return func(self,*fargs,**fkargs,newarg="newarg")
        return newfunc
        #return functools.partial(func,self,newarg="new")

class takeobject(object):
    def __init__(self,func):
        print("called init of takeobject")
        self.func = func

    def __get__(self, obj, owner):
        print("called get of takeobject")
        if obj is None:
            print("get of takeobject return self")
            return self
        self.obj = obj
        self.owner = owner
        print(str(obj))
        print(owner)
        return functools.partial(self.__call__,obj)
        #return function appending __call__ with obj which will append current self to self

    def __call__(self,*args,**kargs):
        print("Called call of takeobject")
        print(args)
        self.func(*args,**kargs)

def simple():
    #print("object passed to simple:" + str(obj))
    print("object passed to simple:")

class testsimple():
    #f = mydeco(simple)

    #@mydeco
    def simple1(self):
        print("object passed to simple:" + str(self))

    #@takeobject
    @mydeco2(delete=True)
    def simple2(self,myarg,newarg):
        print("object passed to simple:" + str(self) + ":" + myarg + ":" + newarg)

    #def __call__(self,*args,**kargs):
    #    print("Called testsimple call")
    #    print(testsimple.f())

#testsimple()()
testsimple().simple2("myarg")
#testsimple()
#class objmethod:
#    @mydeco
#    def mycallobj(self,inputname):
#        print("Called mycallobj")
#        print(f"name={inputname}")
#        print("Called mycallobj")
#
#
#
##objmethod()
#objmethod().mycallobj("username")
#
#@mydeco
#def mycall23():
#    return True
#
#mycall23()

#mycall2("Hello")
