# File management
import pickle
import os

# Data processing
import pandas as pd
import numpy as np
from collections import defaultdict, Counter

# NLP
import random
from scipy import stats
from collections import defaultdict, Counter
import scispacy
import spacy
from spacy_langdetect import LanguageDetector
from spacy.language import Language
import en_core_web_sm
import nltk
from nltk import word_tokenize, pos_tag
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

# Data viz
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


def read_file(data_dir, data_filename):
    """Reads file in pickle format and dumps data into a Dataframe."""
    return pd.read_pickle(os.path.join("../" + data_dir, data_filename))


def set_nlp_pipeline():
    """Sets the components of the SpaCy's NLP pipeline to be used for text preprocessing and analytics."""
    nlp = spacy.load("en_core_web_sm")
    
    @Language.factory('language_detector')
    def language_detector(nlp, name):
        """Sets up a LanguageDetector object to be passed on to the nlp pipeline."""
        return LanguageDetector()
    
    Language.factory("language_detector", func=language_detector)
    nlp.add_pipe('language_detector', last=True)
    
    return nlp



def get_corpus_stats(corpus, nlp):
    """Calculates an array of corpus statistics on the 'text' column, which is the one that contains all the open-ended responses.
    
    Statistics to be computed:
    - # of English docs
    - # of docs in other languages as identified by SpaCy's LanguageDetector()
    - 
    """
    corpus_stats = {}
    other_stats = {}
    
    # token count
    all_tok_count = 0
    en_tok_count = 0
    other_tok_count = 0
    
    # unique tokens
    all_unique_toks = set()
    en_unique_toks = set()
    other_unique_toks = set()
    
    # lang count
    en_docs = 0
    other_lang_docs = 0
    other_langs = []
    other_lang_sents = []  # sample of sentences in "other" languages for further evaluation
    
    for response in corpus:
        doc = nlp(response.replace("\n", ""))
        if doc._.language["language"] == 'en':
            en_docs += 1
            for tok in word_tokenize(response.replace("\n", "")):
                all_tok_count += 1
                en_tok_count += 1
                all_unique_toks.add(tok.lower())
                en_unique_toks.add(tok.lower())
        else:
            other_lang_docs += 1
            other_lang_sents.append(response)
            other_langs.append(doc._.language["language"])
            for tok in response.split(" "):  # most basic split
                all_tok_count += 1
                other_tok_count += 1
                all_unique_toks.add(tok.lower())
                other_unique_toks.add(tok.lower())
    
    
    # consolidates core stats
    corpus_stats["english_docs"] = en_docs
    corpus_stats["other_lang_docs"] = other_lang_docs
    corpus_stats["other_langs"] = set(other_langs)
    corpus_stats["all_token_count"] = all_tok_count
    corpus_stats["en_token_count"] = en_tok_count
    corpus_stats["other_token_count"] = other_tok_count
    corpus_stats["avg_doc_length"] = all_tok_count / len(corpus)
    corpus_stats["all_type_tok_ratio"] = len(all_unique_toks) / all_tok_count
    corpus_stats["en_type_tok_ratio"] = len(en_unique_toks) / en_tok_count
    corpus_stats["other_type_tok_ratio"] = len(other_unique_toks) / other_tok_count
    corpus_stats["all_unique_toks"] = all_unique_toks
    corpus_stats["en_unique_toks"] = en_unique_toks
    corpus_stats["other_unique_toks"] = other_unique_toks
    
    # other stats
    survey_text = " ".join([response for response in corpus])
    other_stats["pos_frequencies"] = pos_counter(survey_text)
    other_stats["lexical_density"] = lexical_density(other_stats["pos_frequencies"], survey_text)
    other_stats["token_probs"] = get_probs(survey_text)
    other_stats["response_lengths"] = avg_response_length(corpus)
    
    return corpus_stats, other_stats, other_lang_sents


def avg_response_length(corpus):
    """Calculates the average length of responses in the corpus."""
    return [len(corpus) / len(response) for response in corpus]


def pos_counter(text):
    """Calculates the relative frequencies of POS tags given the tagged words in the corpus."""
    pos_count = defaultdict(int)
    for _, pos in pos_tag(word_tokenize(text)):
        pos_count[pos] += 1

    return pos_count


def lexical_density(pos_count, text):
    """Calculates the lexical density of the corpus given the frequency of open class prefixes."""
    lexical_den = 0
    open_class_prefix = {"N", "V", "J", "R"}
    
    for pos, count in pos_count.items():
        if pos[0] in open_class_prefix:
            lexical_den += count
            
    return lexical_den / len(text)


def get_probs(all_text):
    """Calculates the relative frequencies off all the tokens in the corpus."""
    counts = Counter(tok.lower() for tok in all_text)
    total = sum(counts.values())
    probs = {word : count / total for word, count in counts.items()}
    
    return probs