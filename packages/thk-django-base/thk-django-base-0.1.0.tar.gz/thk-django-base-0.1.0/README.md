# thk-django-base

Based on django, three-kinds style components.

## Components

### 1. redis

#### 1.1 settings

```python
REDIS = {
    'default': {
        'type': 'standalone',
        'init': {
            'host': 'redis-node-0.redis-headless',
            'port': 6379,
            'db': 0,
            'password': "12345",
            'decode_responses': True
        }
    },
    'sentinel': {
        'type': 'sentinel',
        'init': {
            'sentinels': [
                ('redis-node-0.redis-headless', 26379),
                ('redis-node-1.redis-headless', 26379),
                ('redis-node-2.redis-headless', 26379)
            ],
            'sentinel_kwargs': {
                'password': '12345'
            },
            'password': '12345',
            'db': 1,
            'decode_responses': True,
        },
        'node': {
            'service_name': 'mymaster'
        }
    }
}

```

#### 1.2 usage

```python
from thk_django_base.redis.structures import List
from thk_django_base.redis import RedisFactory

l = List(main_key="l", rdb=RedisFactory.get_rdb("sentinel"))
l.left_push([1, 2, 3], need_exists=True)

```

### 2. natural key

#### 2.1 settings(optional)

```python
NATURAL_KEY = {
    "increment_main_key": "natural_key",
    "random_bit_length": 15,
    "puzzle_count": 100000,
    "redis": "default"
}

```

#### 2.2 usage

```python
from django.db import models
from thk_django_base.model import NKModel


class Book(NKModel):
    name = models.CharField(max_length=32, db_index=True)

```


### 3. others

* field_utils: PathWithIDName
* validators: FileMaxSizeValidator
