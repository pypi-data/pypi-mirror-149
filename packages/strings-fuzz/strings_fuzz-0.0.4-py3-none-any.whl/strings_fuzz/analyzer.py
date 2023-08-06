# Import libraries

import pandas as pd
import numpy as np
import collections
import string
import pythainlp
from cleaner import is_symbols_only

# Check frequencies

def tokenize(a, delimiter=" "):
    if pd.isnull(a) or a == "":
        return a
    elif delimiter == "":
        return list(a)
    else:
        return a.split(delimiter)

def n_gram(a, n, delimiter=" "):
    if pd.isnull(a) or a == "":
        return None
    else:
        tokens = tokenize(a, delimiter)
        ngrams = zip(*[tokens[i:] for i in range(n)])
        return [delimiter.join(ngram) for ngram in ngrams]
    
def flatten(list):
    return [item for sublist in list for item in sublist]

def n_grams(list, n, delimiter=" "):
    return flatten([n_gram(x, n, delimiter) for x in list])

def most_common(list):
    counter = collections.Counter(list)
    return counter.most_common()

def filter_array(predicate, array):
    np_array = np.array(array)
    filtered_indices = np.vectorize(predicate)(np_array)
    return np_array[filtered_indices]

def is_english(a):
    if pd.isnull(a) or a == "":
        return False
    else:
        return not is_symbols_only(a) and a.replace("–", "").isascii()

def is_thai(a):
    if pd.isnull(a) or a == "":
        return False
    else:
        punctuation_digits = string.punctuation + " " + string.digits + "–"
        return not is_symbols_only(a) and np.all([c in pythainlp.thai_characters or c in punctuation_digits for c in a])

def filter_english(array):
    return filter_array(is_english, array)

def filter_thai(array):
    return filter_array(is_thai, array)