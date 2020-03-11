# generator
def uc_gen(text):
    for char in text:
        yield char.upper()

# generator expression
def uc_genexp(text):
    return (char.upper() for char in text)

# iterator protocol
class uc_iter():
    def __init__(self, text):
        self.text = text
        self.index = 0
    def __iter__(self):
        return self
    def __next__(self):
        try:
            result = self.text[self.index].upper()
        except IndexError:
            raise StopIteration
        self.index += -1 if self.index < 0 else 1
        return result

    def __reversed__(self):
        self.index = -1
        return self

    def __len__(self):
        return len(self.text)

# getitem method
class uc_getitem():
    def __init__(self, text):
        self.text = text
    def __getitem__(self, index):
        result = self.text[index].upper()
        return result
    def __len__(self):
        return len(self.text)


            
#for iterator in uc_gen, uc_genexp, uc_iter, uc_getitem:
for iterator in uc_iter, uc_getitem:
    for ch in reversed(iterator('abcde')):
        print(ch,end=" ")
    print("")
