class Tokenizer:
    """Tokenize text"""
    def __init__(self, *argv):
        print('Start init Tokenizer.__init__()')
        #if self.tokens is not None:
        #    self.tokens += text.split()
        #else:
        #    self.tokens = text.split()
        print(argv)
        #self.tokens = argv[0].split()
        #self.cls = argv[0]
        self.count = argv[0]
        print('End init Tokenizer.__init__()')


class WordCounter(Tokenizer):
    """Count words in text"""
    def __init__(self, text):
        print('Start init WordCounter.__init__()')
        #super().__init__(text + " wordcounter", WordCounter)
        #super().__init__(text + " wordcounter")
        super().__init__(text)
        #super(WordCounter,self).__init__(text + " wordcounter", WordCounter)
        #self.word_count = len(self.tokens)
        print('End init WordCounter.__init__()')


class Vocabulary(Tokenizer):
    """Find unique words in text"""
    def __init__(self, text):
        print('Start init Vocabulary.__init__()')
        #super().__init__(text + " vocabulary", Vocabulary)
        print(text)
        super().__init__(len(text)+2)
        #super(Vocabulary,self).__init__(text + " vocabulary", Vocabulary)
        #self.vocab = set(self.tokens)
        print('End init Vocabulary.__init__()')


class TextDescriber(WordCounter, Vocabulary):
    """Describe text with multiple metrics"""
    def __init__(self, text):
        print('Start init TextDescriber.__init__()')
        super().__init__(text + " text ")
        #super(TextDescriber,self).__init__(text + " text ")
        print('End init TextDescriber.__init__()')


td = TextDescriber('row row row your boat')
print(TextDescriber.mro()) #super keyword will follow the MRO chain of calling methods
print(WordCounter.mro())
print(Vocabulary.mro())
#print('--------')
#print(td.tokens)
#print(td.vocab)
#print(td.word_count)
#print(td.cls)
print(td.count)
