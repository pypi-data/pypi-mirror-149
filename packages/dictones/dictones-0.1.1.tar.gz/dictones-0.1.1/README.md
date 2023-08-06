
## Description

Like dict, but a little bit better

# install
```
  pip install dictones
```

#### import

```python
from dictones import DictOnes
```

#### Usage
# 1. Added constructor
```python
  filled_dict = DictOnes('first_key, second_key', 'to first key', 'to second key')
  print(filled_dict.first_key)
  print(filled_dict.second_key)
```

#### Output

```http
'to first key'
'to second_key'
```

# 2. Constructor without filling
```python
  filled_dict = DictOnes('first_key, second_key')
  print(filled_dict.first_key)
  print(filled_dict.second_key)
  print(filled_dict.key)
```

#### Output

```http
None
None
...raise KeyError(attrname)
KeyError: 'key'
```

# 3. Deleting
```python
filled_dict = DictOnes('first_key, second_key')
print(filled_dict.first_key)
print(filled_dict.second_key)
print('second_key' in filled_dict)
del filled_dict.second_key
print('second_key' in filled_dict)
```
#### Output
```http
None
None
True
False
```

# Otherwise it is the same dict