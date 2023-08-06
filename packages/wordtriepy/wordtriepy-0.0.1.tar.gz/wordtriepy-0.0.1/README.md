## WordTriePy

This is a small Python package that implements a trie filled with words from several languages (English - en, German - de , French - fr, Spanish - es, Portuguese - pt) implemented as nested dictionaries. It was created in need for a personal project and published to eventually help others.

## Install

```pip install wordtriepy```

## Usage

To find all characters that could follow the partial word "chair" in the English language, use the `get_next_chars()` method:

```python
from wordtriepy import WordTrie

t = WordTrie()
print(t.get_next_chars("chair"))
# outputs: ['_end', 'e', 'l', 'm', 'w']
```

The `_end` token tells us that "chair" itself is a valid word and there are 4 other characters ('e', 'l', 'm', 'w') that could follow the word "chair" in the English language that could form new valid words.

To get a list of words that can be formed by the partial word "salz" in the German language, use the `get_next_words()` method:

```python
from wordtriepy import WordTrie

t = WordTrie(language="de")
print(t.get_next_words("salz", topn=5))
# outputs: ['salz', 'salze', 'salzt', 'salzen', 'salzes']
```

This returns the top 5 words after a breadth-first-search in the German word trie.