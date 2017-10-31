# Simhash

How to compute the similarity between two documents using Localy Sensitive Hashing (LSH):
`cat main.py`

```python
from simhash import Simhash

text1 = 'Hi, how are you ?'
text2 = 'Hi, how are you darling ??

lsh1 = Simhash(text1)
lsh2 = Simhash(text2)

sim = lsh1.distsim(lsh2)

print("Similarity (in [0,1]) between text1 and text2 : %s" % (sim))
```


