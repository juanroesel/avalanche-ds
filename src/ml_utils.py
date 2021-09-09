# File management
import joblib
import os
from datetime import datetime

# Data processing
import numpy as np
import pandas as pd
from collections import defaultdict

# Machine Learning
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.model_selection import GridSearchCV

# BERT
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

# Data Viz
from pprint import pprint

# NLP imports
from nlp_pipeline import *


def responses_to_vectors(data):
    """Pre-processes open-ended responses and converts them to vectors."""
    responses = [lemmatization(preprocess(text)) for text in data["text"].dropna()]
    vectorizer = CountVectorizer(
        lowercase=True, token_pattern='[a-zA-Z0-9]{3,}', analyzer="word", stop_words="english", min_df=3, 
        max_df=0.1, ngram_range=(1, 3)
    )
    X = vectorizer.fit_transform(responses)
    
    return X, vectorizer


def implement_lda(X, vectorizer, max_iter=500):
    """Implements the LDA algorithm to the vectorized responses to run topic modeling."""
    lda_model = LatentDirichletAllocation(n_components=5, learning_method="online", max_iter=max_iter,
                                          evaluate_every=1, verbose=1, random_state=20)
    theta = lda_model.fit_transform(X)
    top20_theme_words = []
    for i in range(lda_model.components_.shape[0]):
        arr = lda_model.components_[i, :]
        print()
        print(f"Theme No.: {i}")
        print(f"Sum of corresponding row: {np.sum(arr)}")
        top_20 = arr.argsort()[-20:][::-1]
        data = []
        words = []
        for j in range(top_20.shape[0]):
            for word, idx in vectorizer.vocabulary_.items():
                if idx == top_20[j] and top_20[j] >= 5:
                    words.append(word)
                    data.append({"x": word, "y": round(arr[idx], 2)})
        print(f"Top 20 words: {words}")
        print("--------------------------------------------")
        top20_theme_words.append({
            "theme #": i,
            "data": data
        })
        
    return lda_model, top20_theme_words


def create_theme_matrix(X, lda_model, data):
    """Creates theme matrix DataFrame, where rows are documents and columns are theme probabilities."""
    # Create Document - Theme Matrix
    lda_output = lda_model.transform(X)
    # column names
    theme_ids = ["Theme" + str(i) for i in range(lda_model.n_components)]
    # index names
    doc_ids = ["Doc" + str(i) for i in range(len(data["text"].dropna()))]
    # Make the pandas dataframe
    df_document_themes = pd.DataFrame(np.round(lda_output, 2), columns=theme_ids, index=doc_ids)
    # Get dominant theme for each document
    dominant_theme = np.argmax(df_document_themes.values, axis=1)
    df_document_themes['dominant_theme'] = dominant_theme
    
    return df_document_themes


def get_theme_documents(data, df_document_themes, N):
    """Returns a list of documents relevant to the theme cluster N."""
    cluster_idx = df_document_themes.groupby("dominant_theme").get_group(N).index.to_list()
    cluster_idx = [int(idx.strip("Doc")) for idx in cluster_idx]
    theme_docs = [preprocess(text) for i, text in enumerate(data["text"]) if i in cluster_idx]
    
    return theme_docs


def color_green(val):
    """Applies styling to the DataFrame."""
    color = 'green' if val > .1 else 'black'
    return 'color: {col}'.format(col=color)


def make_bold(val):
    """Makes a particular piece of text bold."""
    weight = 700 if val > .1 else 400
    return 'font-weight: {weight}'.format(weight=weight)
