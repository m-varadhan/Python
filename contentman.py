import unittest
from time import time, sleep

class Timed():
    """A simple "timer" context manager. It prints execution time."""
    def __init__(self,arg):
        self.arg = arg
        pass

    def __enter__(self):
        self.start = time()
        print("Starting at {}".format(self.start))
        return self #****************return self or object used by with 'as' assignment

    def __exit__(self, type, value, traceback):
        # This code is guaranteed to run
        if traceback:
            print("type: {}".format(type))
            print("value: {}".format(value))
            print("traceback: {}".format(traceback))

        self.end = time()
        total = self.end - self.start
        print("Ending at {} (total: {})".format(self.end, total))

    def print_this(self,msg):
        print(self.arg)
        print(msg)

def mygen():
    for i in range(100,105): yield  i

class mytest(unittest.TestCase):
    def setUp(self):
        pass

    def testmytest(self):
        for i in range(1,10):
            for k in mygen():
                with Timed("arg") as t:
                    t.print_this("sleeping for 2...")
                    sleep(2)
    
    def tearDown(self):
        pass

def suite():
    suite = unittest.TestSuite()
    suite.addTest(mytest('testmytest'))
    return suite

def run():
    runner = unittest.TextTestRunner()
    runner.run(suite())

if __name__ == '__main__':
    run()

