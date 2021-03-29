import pandas as pd
import numpy as np
import re
import os
import sys
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder

class TuristRecommender():
    def __init__(self):
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models/model.pickle'), 'rb') as handle:
            self.__model = pickle.load(handle)
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models/vectorizer.pickle'), 'rb') as handle:
            self.__vectorizer = pickle.load(handle)
        self.__dataframe = pd.read_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dataset/kazakhstan_travel_kz.csv'))


    def cleaning_data(self, code_data):
        text = code_data
        text = text.replace('(<br/>)', '')
        text = text.replace('(<a).*(>).*(</a>)', '')
        text = text.replace('(&amp)', '')
        text = text.replace('(&gt)', '')
        text = text.replace('(&lt)', '')
        text = text.replace('(\xa0)', ' ')
        text = text.replace('-', ' ')
        text = text.replace('(', ' ')
        text = text.replace(')', ' ')
        text = self.filtering(text)
        return text.strip()

    def filtering(self, text):
        stripped = re.sub('[^a-zA-Z, ^А-Я,а-я,Ә,І,Ң,Ғ,Ү,Ұ,Қ,Ө,Һ,ә,і,ə,ң,ғ,ү,ұ,қ,ө,һ]', ' ', str(text).replace('-', ''))
        stripped = re.sub('_', '', stripped)
        stripped = re.sub('\s+', ' ', stripped)
        return str(stripped).lower()
    
    def predict(self, text):
        text = self.cleaning_data(text)

        predictions = self.__model.predict_proba(self.__vectorizer.transform([text]).toarray())
        return self.__dataframe[self.__dataframe['label_cat'].isin((-predictions[0]).argsort()[:5])]['url'].values.tolist()