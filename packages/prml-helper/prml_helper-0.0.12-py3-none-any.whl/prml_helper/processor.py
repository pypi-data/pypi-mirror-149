import numpy as np
import pandas as pd
import re
import nltk
from sklearn.base import BaseEstimator, TransformerMixin
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
nltk.download('wordnet')
import string

class Preprocessor(BaseEstimator, TransformerMixin):
  def __init__(self):
    self.stop_words_ = stopwords.words('english')
    self.word_lemmatizer_ = WordNetLemmatizer()
    print("Started Pre-Processing")

  def cleanHtmltags(self, sentence):
    cleanr = re.compile('<.*?>')
    cleanr = re.compile('https?://\S+|www\.\S+')
    cleanedtext = re.sub(cleanr, ' ', str(sentence))
    return cleanedtext
  
  def cleanPunc(self, sentence):
    sentence = "".join([word for word in sentence if word not in string.punctuation])
    sentence = sentence.strip()
    cleaned = sentence.replace("\n"," ")
    return cleaned

  def fit(self, X, y = None):
    return self

  def transform(self, X, y = None):
    X = X["comment_text"]
    X = X.str.lower()
    X = X.apply(self.cleanHtmltags)
    X = X.apply(self.cleanPunc)
    X = X.apply(lambda x: " ".join([word for word in x.split() if word.lower() not in self.stop_words_]))
    X = X.apply(lambda x: " ".join([self.word_lemmatizer_.lemmatize(word) for word in x.split()]))
    return X