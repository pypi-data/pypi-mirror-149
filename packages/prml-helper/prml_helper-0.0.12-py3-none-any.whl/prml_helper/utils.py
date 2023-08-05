

import numpy as np
import pandas as pd
import re
import nltk
from sklearn.base import BaseEstimator, TransformerMixin
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
nltk.download('wordnet')
lemmatizer = WordNetLemmatizer()


class TrainPreprocess(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.stop = stopwords.words('english')

    def clean_text(self,text):
        text = str(text)
        text = re.sub(r'[0-9"]', '', text) # number
        text = re.sub(r'#[\S]+\b', '', text) # hash
        text = re.sub(r'@[\S]+\b', '', text) # mention
        text = re.sub(r'https?\S+', '', text) # link
        text = re.sub(r'\s+', ' ', text) # multiple white spaces
        text = re.sub(r'\W+', ' ', text) # non-alphanumeric
        return text.strip()

    def lemmatize_text(self,x):
        return ' '.join([lemmatizer.lemmatize(word) for word in str(x).split()])
    
    def stop_remove(self,x):
        return ' '.join([word for word in x.split() if word not in (self.stop)])
    
    def remove_na(self):
        self.X.dropna()
    
    def fit(self,X,Y=None):
        self.X = X
        self.X = self.X.str.lower()
        # self.remove_na()
        return self
    
    def transform(self,X):
        self.X = X
        self.X = self.X.str.lower()
        self.X = self.X.apply(lambda x: self.clean_text(x))
        self.X = self.X.apply(lambda x: ' '.join([word for word in x.split() if word not in (self.stop)]) )
        self.X = self.X.apply(lambda x: ' '.join([lemmatizer.lemmatize(word) for word in str(x).split()]))
        return self.X
