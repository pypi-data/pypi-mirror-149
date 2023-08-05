# Import libraries
import pandas as pd
import re
from num2words import num2words

# Clean stopwords
def replace_pattern(pattern, replacement, s, **kwargs):
    if pd.isnull(s):
        return s
    else:
        return re.sub(pattern, replacement, str(s), **kwargs)

def replace_whole_word(word, replacement, s, **kwargs):
    return replace_pattern(rf'\b{word}\b', replacement, s, **kwargs)

default_stopwords = pd.read_csv('src/strings_fuzz/data/stop_words.csv')
default_stopwords = default_stopwords.to_dict('records')

def process_stopwords(s, stopwords=default_stopwords, **kwargs):
    result = s
    for stopword in stopwords:
        action = stopword['action']
        word = stopword['word']
        whole_word = stopword['whole_word']

        if action in ['replace', 'remove']:
            if action == 'replace':
                replacement = stopword['replacement']
            else:
                replacement = ""
            if whole_word:
                result = replace_whole_word(word, replacement, result, **kwargs)
            else:
                result = replace_pattern(word, replacement, result, **kwargs)
    return result

# Define cleaner function
def replace_non_breaking_space(s):
    return replace_pattern(r"\xa0", " ", s)

def remove_leading_symbols(s):
    return replace_pattern(r"^([^\w\(]|_)+", "", s)

def remove_trailing_symbols(s):
    return replace_pattern(r"([^\w\)]|_)+$", "", s)

def trim(s):
    return remove_leading_symbols(remove_trailing_symbols(s))

def replace_multiple_spaces(s):
    return replace_pattern(r"\s{2,}", " ", s)

def remove_empty_parenthesis(s):
    return replace_pattern(r"[\(\[]\s*[\)\]]", "", s)

def remove_space_start_parenthesis(s):
    return replace_pattern(r"(?<=[\[\(])\s+", "", s)

def remove_space_end_parenthesis(s):
    return replace_pattern(r"\s+(?=[^\S]*[\]\)])", "", s)

def remove_space_parenthesis(s):
    return remove_space_start_parenthesis(remove_space_end_parenthesis(s))

def clean_mess(s):
    return trim((replace_multiple_spaces(remove_space_parenthesis(remove_empty_parenthesis(replace_non_breaking_space(s))))))

# Set meaningless names to null

def is_symbols_only(s):
    if pd.isnull(s) or s == "":
        return False
    else:
        return not bool(re.compile(r"(?=[^\W_])").search(str(s)))

def is_single_character(s):
    if pd.isnull(s) or s == "":
        return False
    else:
        return len(str(s)) == 1

def is_numbers_and_symbols_only(s):
    if pd.isnull(s) or s == "":
        return False
    else:
        one_to_twenty = [num2words(x) for x in range(21)]
        tens = [num2words(x) for x in range(20, 91, 10)]
        other_num_words = ['hundred', 'thousand', 'million', 'billion']
        num_words = one_to_twenty + tens + other_num_words

        str_input = str(s)
        nums_or_numwords_or_symbols = re.compile(rf"([0-9]|({'|'.join(num_words)})|and|[^\w]|_)*", flags=re.IGNORECASE)
        return nums_or_numwords_or_symbols.search(str_input).group(0) == str_input
    
def remove_meaningless(s):
    if is_numbers_and_symbols_only(s) or is_single_character(s) or is_symbols_only(s):
        return None
    else:
        return s