from lib2to3.pgen2 import token
from nltk.tokenize import word_tokenize
import nltk
nltk.download('stopwords', quiet=True)
from nltk.corpus import stopwords
stopwords = list(stopwords.words('english'))
import contractions

def get_keywords(text):
    text = text.lower()
    text = ' '.join([contractions.fix(word) for word in text.split()])
    tokens = word_tokenize(text) 
    keyword_filter = lambda token: (not token in stopwords) and len(token) > 1 and token.isalpha()
    keywords = list(filter(keyword_filter, tokens))
    return keywords
