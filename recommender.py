import streamlit as st
import dill as pickle
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from nltk.stem import SnowballStemmer
import re

# Loading the saved model, vectorizer, tokenizer
knn = pickle.load(open('models/knn_model.sav', 'rb'))
tfidf = pickle.load(open('models/tfidf.sav', 'rb'))

# Load in review dataframe; necessary in order to extract artist name for recommendation
total_df = pd.read_csv('data/reviews_w_lang.csv')
total_df = total_df[total_df['lang'] == 'en']


def prepare(review):
    '''
    Takes a user inputted review/blurb, and uses the saved TF-IDF vectorizer and KNN model to recommend an album

    Args:
        review (string)

    Returns:
        recommendation (string)
    '''

    # receive input
    review = str(review)
    
    # transformed input
    review_transformed = tfidf.transform(pd.Series(review))
    
    # use model.predict to recommend album
    recommend_album = knn.predict(review_transformed)[0]
    
    # find associated artist
    recommend_artist = total_df[total_df['album'] == f'{recommend_album}']['ars_name'].unique()[0]
    
    # make album titlized
    recommend_album = recommend_album.replace('-', ' ')
    recommend_album = recommend_album.replace('_', ' ')
    recommend_album = recommend_album.title()
    
    # make artist name titlized
    recommend_artist = recommend_artist.replace('-', ' ')
    recommend_artist = recommend_artist.replace('_', ' ')
    recommend_artist = recommend_artist.title()
    
    # save recommendation
    recommendation = f"We recommend the album '{recommend_album}' by {recommend_artist}"
    
    return recommendation
 
       
def main():
    '''
    Initializes Streamlit application with title, text input area, and a button to generate recommendation.
    When pressed, button causes input to be processed by prepare(), and the output recommendation is displayed
    '''

    st.title('Write a Review, Get a Recommendation')
    
    review = st.text_input("Write a small blurb about why you like a certain \
                           piece of music (without explicitly naming the piece \
                                           or artist), or just some adjectives \
                                           you want to describe your music recommendation. \
                                           We'll give you an \
                               album to check out!")
    
    recommendation = ''
    
    if st.button('Generate my recommendation!'):
        recommendation = prepare(review)
        
    st.success(recommendation)
    
    
if __name__ == '__main__':
    '''
    Runs Streamlit application
    '''
    main()