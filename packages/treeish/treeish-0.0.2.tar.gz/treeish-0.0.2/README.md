# Treeish

Some functions to help with tree like (json-ish) python structures.

## Example Data

```python
>>> data = [
        {
            "item": "Preliminary Title",
            "units": [
                {
                    "item": "Chapter 1",
                    "caption": "Effect and Application of Laws",
                    "units": [
                        {
                            "item": "Article 1",
                            "content": 'This Act shall be known as the "Civil Code of the Philippines." (n)\n',
                        },
                        {
                            "item": "Article 2",
                            "content": "Laws shall take effect after fifteen days following the completion of their publication either in the Official Gazette or in a newspaper of general circulation in the Philippines, unless it is otherwise provided. (1a)\n",
                        },
                    ],
                }
            ],
        }
    ]
```

## Setter of IDs

```python
>>> from treeish import set_node_ids
>>> set_node_ids(data)
# all nodes in the tree will now have an `id` key, e.g.:
{
    "item": "Article 1",
    "content": 'This Act shall be known as the "Civil Code of the Philippines." (n)\n',
    "id": "1.1.1.1"
},
```

## Getter of Node by ID

```python
>>> from treeish import get_node_id
>>> get_node_id("1.1.1.1")
{
    "item": "Article 1",
    "content": 'This Act shall be known as the "Civil Code of the Philippines." (n)\n',
}
```

## Fetcher of Values

```python
>>> from treeish import test_fetch_values_from_key
>>> list(test_fetch_values_from_key(data[0]), "item")
[
    "Preliminary Title",
    "Chapter 1",
    "Article 2",
    "Article 1",
]
```
