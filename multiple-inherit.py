class A(object):
    def __init__(self, i, **kwargs):
        print("called A __init__")
        #super(A, self).__init__(**kwargs)
        super().__init__(**kwargs)
        self.i = i
    def run(self, value):
        return self.i * value

class B(A):
    def __init__(self, j, **kwargs):
        print("called B __init__")
        super(B, self).__init__(**kwargs)
        self.j = j
    def run(self, value):
        return super(B, self).run(value) + self.j

class Logger(object):
    def __init__(self, name, **kwargs):
        print("called Logger __init__")
        super(Logger,self).__init__(**kwargs)
        self.name = name
    def run_logged(self, value):
        print("Running", self.name, "with info", self.info())
        return self.run(value)

class BLogged(B, Logger):
    def __init__(self, **kwargs):
        print("called BLogger __init__")
        super(BLogged, self).__init__(name="B", **kwargs)
    def info(self):
        return 42

print(BLogged.mro())
b = BLogged(i=3, j=4)
