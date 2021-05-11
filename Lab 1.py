import nltk
import ssl
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
nltk.download()

# Test NLTK – Brown Corpus
from nltk.corpus import brown
print(brown.words()[0:10])
print(len(brown.words()))

# Test NLTK – Book Resources
from nltk.book import *
print(texts())
print(len(text1))



