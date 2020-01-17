import logging

class log:
    def __init__(self,name=None):
        self.logger = None
        if not name:
            return
        init(name)

    def init(self,name):
        self.logger=logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

    def __get__(self):
        return self.logger

    def __getattr__(self,attr):
        return eval('self.logger.'+attr)

logger = log()
