# Brandenburg

The code behind *The RGM Files*, a series of case studies in revenue growth
management: the work of deciding what a consumer-goods company charges, which
pack sizes it sells, when it promotes and what it agrees with retailers.

Each episode takes one real decision by a well-known brand, sets out what the
company did and what happened in public numbers, and models the decision so you
can change the inputs and see what else would have happened. The interactive
version of each model runs in the browser at caspase.ai. This repository holds
the reference model in Python, its data with a source for every number, and
tests that check the page and the Python agree.

## Episodes

| # | case | page | folder |
|---|---|---|---|
| 1 | Hershey's price decision, August 2024 | [caspase.ai/hershey](https://caspase.ai/hershey/) | [`episodes/01-hershey`](episodes/01-hershey) |

## Run an episode

```
cd episodes/01-hershey
python3 tests/test_numbers.py
```

Each episode's README says what else it runs and what it needs.

## Licence

MIT. Fork it, change it, use it. See `LICENSE`.
