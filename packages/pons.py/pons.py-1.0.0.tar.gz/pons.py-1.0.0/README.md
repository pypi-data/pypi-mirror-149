<div align="center">
  <h1>pons.py</h1>
  An API wrapper for the PONS dictionary written in Python
</div>

## Installation
```sh
$ pip install pons.py
```

## Usage
```py
from pons import Client

pons = Client("YOUR_SECRET")  # see PONS API reference

# get dictionaries
# params: language (de|el|en|es|fr|it|pl|pt|ru|sl|tr|zh)
dictionaries = pons.get_dictionaries("en")        # returns a list of Dictionary objects

# get translations
# required params: term, dictionary, source language
# optional params: output language, fuzzy (bool), references (bool)
entries = pons.query("term", "deen", "en")["en"]  # returns a list of EntryHit objects
entries[0].translations                           # returns a list of translations (strings)
```

## References
- [PONS API Reference](https://en.pons.com/p/online-dictionary/developers/api)
- [API Documentation](https://en.pons.com/p/files/uploads/pons/api/api-documentation.pdf)
