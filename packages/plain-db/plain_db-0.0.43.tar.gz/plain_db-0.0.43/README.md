# plain_db

Plain txt db

## usage

```
import plain_db
counter = plain_db.load('counter')
counter.update('abc', 2)
counter.inc('abc', 1)
counter.get('abc') # 3
```

## how to install

`pip3 install plain_db`