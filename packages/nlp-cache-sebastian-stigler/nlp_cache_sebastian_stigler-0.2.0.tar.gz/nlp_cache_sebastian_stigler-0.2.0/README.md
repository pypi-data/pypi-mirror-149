# NLP Cache

A caching component for `Doc` classes in `spacy`

# Installation

```bash
pip install nlp_cache_sebastian_stigler
```

# Usage

```python
import spacy

nlp = spacy.load("de_core_news_sm")
text = "Ich wünsche Ihnen einen guten Morgen!"
doc_1 = nlp(text)  # mean loading time about 4.5 ms
doc_2 = nlp(text)  # recurrent mean loading time about 4.5 ms
```

To speed up loading a recurrent text you can use this caching utility, to
lookup known texts from the cache stored in the `cache` directory .

```python
import spacy
from nlp_cache import NlpCache

nlp = NlpCache(uncached_nlp=spacy.load("de_core_news_sm"), path="cache")
text = "Ich wünsche Ihnen einen guten Morgen!"
doc_1 = nlp(text)  # mean loading time about 4.5 ms
doc_2 = nlp(text)  # recurrent mean loading time about 840 µs
```
