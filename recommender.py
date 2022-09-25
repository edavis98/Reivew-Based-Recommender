# -*- coding: utf-8 -*-
"""
Created on Wed Sep  7 21:17:17 2022

@author: evanm
"""

import streamlit as st
import dill as pickle
import pandas as pd
import re
from sklearn.neighbors import KNeighborsClassifier
from nltk.stem import SnowballStemmer

# Loading the saved model, vectorizer, tokenizer
knn = pickle.load(open('models/knn_model.sav', 'rb'))
tfidf = pickle.load(open('models/tfidf.sav', 'rb'))

# Load in review dataframe; necessary in order to extract artist name for recommendation
total_df = pd.read_csv('data/reviews_w_lang.csv')
total_df = total_df[total_df['lang'] == 'en']


def prepare(review):
    
    review = str(review)
    
    review_transformed = tfidf.transform(pd.Series(review))
    
    recommend_album = knn.predict(review_transformed)[0]
    
    recommend_artist = total_df[total_df['album'] == f'{recommend_album}']['ars_name'].unique()[0]
    
    # Make album title look nice
    recommend_album = recommend_album.replace('-', ' ')
    recommend_album = recommend_album.replace('_', ' ')
    recommend_album = recommend_album.title()
    
    # Make artist name look nice
    recommend_artist = recommend_artist.replace('-', ' ')
    recommend_artist = recommend_artist.replace('_', ' ')
    recommend_artist = recommend_artist.title()
    
    recommendation = f"We recommend the album '{recommend_album}' by {recommend_artist}"
    
    return recommendation
 
       
def main():
    
    st.title('Write a Review, Get a Recommendation')
    
    review = st.text_input("Write a small blurb about why you like a certain \
                           piece of music (without explicitly naming the piece \
                                           or artist), and we'll give you an \
                               album to check out!")
    
    recommendation = ''
    
    if st.button('Generate my recommendation!'):
        recommendation = prepare(review)
        
    st.success(recommendation)
    
    
if __name__ == '__main__':
    main()