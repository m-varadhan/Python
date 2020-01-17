class BaseVector2D(object):
    def __new__(cls, *args, **kw):
        print("Called BaseVector2D __new__"+repr(cls) )
        print(type(cls))
        #return super().__new__(cls,*args,**kw)
        return super(BaseVector2D,cls).__new__(cls)
        #return super(BaseVector2D,cls).__new__(cls,*args,**kw)

class Vector2D(BaseVector2D):
    def __new__(cls, *args, **kw):
        print("Called Vector2D __new__"+repr(cls) )
        print(type(cls))
        print(args)
        print(kw)
        return super(Vector2D,cls).__new__(cls,*args,**kw)
        #return super().__new__(cls)

    def __call__(cls,*args,**kw):
        print("Called __call__")

    def __prepare__(cls,*args,**kw):
        print("Called __call__")

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "X:" + str(self.x) + ",Y:" + str(self.y)

vec = Vector2D(1,2)
print("Printing vec:",vec)
