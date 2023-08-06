# Strings-Fuzz

A flexible fuzzy string matcher that finds best matches between two sets using the edit distance method. It provides useful NLP methods to help identify stopwords to be replaced or removed in each set as well as some default stopwords for different types of data.

## Language Support

Currently supports Enlish and Thai.

## Installation

Run the following to install:

```python
pip install strings-fuzz
```

## Usage

```python
from strings_fuzz import cleaner

# Trims trailing symbols and spaces
cleaner.trim("...+=    Hello World   . ")
```

# Developing Strings-Fuzz

To install strings-fuzz along with the tools you need to develop and run tests, run the following in your virtualenv:

```bash
$ pip install -e .[dev]
```
