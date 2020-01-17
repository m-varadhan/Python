#def init_attributes(name, bases, idict):
class InitAttributes(type):

    #def __call__(cls, *args, **kwargs): #on class instance creation of meta's subclass
    #    pass

    def __init__(cls, name, bases, idict): #on class instance creation of meta's subclass
        print('The Class Name is', name)
        print('The Class Bases are', bases)
        print('The idict has', len(idict), 'elems, the keys are', idict.keys())
        if 'attributes' in idict:
            for attr in idict['attributes']:
                idict[attr] = 1

    #return type(name, bases, idict)

#class Initialised(object):
#    __metaclass__ = init_attributes
#    attributes = ['foo', 'bar', 'baz']

#class Initialised(object,metaclass=init_attributes):
class Initialised(object,metaclass=InitAttributes):
    #__metaclass__ = init_attributes
    attributes = ['foo', 'bar', 'baz']

print('foo =>', vars(Initialised))
print('foo =>', Initialised.foo)
