class B:
    def __init__(self):
        print('__init__: B:' + str(id(self)))
        self.b = "B"
        pass
    def x(self):
        print('x: B:' + str(id(self)))


class C:
    def __init__(self):
        self.c = "C"
        print('__init__: C:' + str(id(self)))
        pass
    def x(self):
        print('x: C:' + str(id(self)))


class D(C, B):
    def __init__(self):
        print('__init__: D:' + str(id(self)))
        super().__init__() # == super(D,self).__init__() 
        super(C,self).__init__() #== #B.__init__(self)
        pass

    def x(self):
        print('x: D:' + str(id(self)))
        B.x(self)
        C.x(self)


d = D()
d.x()
print(d.c)
print(d.b)
print(D.mro())
