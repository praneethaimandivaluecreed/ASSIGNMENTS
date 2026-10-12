# from unittest.mock import Mock

# api = Mock()

# api.get_products.return_value = [
#     {"id": 1, "name": "Phone"}
# ]

# result=api.get_products()
# results=api.get_products.assert_called_once()
# print(result)
import random
import pytest

def add(a,b):
    return random.randint(a,b)

def test_add():
    assert add(1 , 10)==5