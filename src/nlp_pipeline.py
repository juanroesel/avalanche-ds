# NLP
import re
from nltk.stem import WordNetLemmatizer
from nltk import word_tokenize


def preprocess(text):
    """Cleans text from special characters."""
    # removing new line characters
    text = re.sub('\n ','', str(text))
    text = re.sub('\n',' ', str(text))
    text = re.sub('\n\n',' ', str(text))
    # removing apostrophes
    text = re.sub("'s",'', str(text))
    # removing hyphens
    text = re.sub("-",' ', str(text))
    text = re.sub("— ",'', str(text))
    # removing quotation marks
    text = re.sub('\"','', str(text))
    # removing salutations
    text = re.sub("Mr\.",'Mr', str(text))
    text = re.sub("Mrs\.",'Mrs', str(text))
    # removing any reference to outside text
    text = re.sub("[\(\[].*?[\)\]]", "", str(text))
    # removing ampersand
    text = text.replace('&amp;amp;', '&')
    # removing &amp;#x200B
    text = text.replace('&amp;#x200B', '')
    # removing &lt
    text = text.replace('&lt;', '')
    
    return text


def lemmatization(text):
    """Lemmatizes word using NLTK lemmatizer object."""
    lemmatizer = WordNetLemmatizer()
    lemmas = [lemmatizer.lemmatize(tok) for tok in word_tokenize(text)]
    
    return " ".join(lemmas)