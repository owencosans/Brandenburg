# Episode 1: Hershey's price decision, August 2024

Cocoa prices more than doubled in 2024. In August Hershey raised prices, about
6.5% on average across its range, before it knew what Mars would do. Mars then
raised prices 10 to 11%. This model asks whether Hershey hit the 2025 goal its
guidance implied, and what other price moves would have done.

- The page: [caspase.ai/hershey](https://caspase.ai/hershey/)
- Every source and every limit: [caspase.ai/hershey/sources](https://caspase.ai/hershey/sources/)

## Files

- `model.py`: the model, about sixty lines.
- `fit_switching.py`: how the switching number was fitted to Hershey's volume
  before the decision.
- `data/sources.csv`: every input, with its value, whether it is confirmed,
  reported, a best estimate or derived, its source and when it was published.
- `tests/test_numbers.py`: recomputes every number the page publishes.
- `tests/test_parity.py`: checks that the page's JavaScript gives the same
  numbers as `model.py`.

## Run it

Python 3.9 or later; the model and `fit_switching.py` need nothing else.

```
python3 tests/test_numbers.py
python3 fit_switching.py
pip install playwright && playwright install chromium && python3 tests/test_parity.py
```

## How it works

- **Two sides of the shelf.** Hershey, with 45% of US chocolate, and everyone
  else, whose price moves with Mars.
- **Volume changes for two reasons.** People buy less chocolate when all of it
  costs more (category elasticity, best estimate −0.5). And people switch
  between the two sides when their prices move apart (a logit on the log of
  each side's price change, switching 1.25).
- **Cost per unit is fixed** at what Hershey's hedges delivered in 2025.
- **Gross profit** is 2024 net sales × price × volume × margin, set against the
  $4.15bn Hershey's February 2025 guidance implies: net sales up at least 2%,
  and gross margin down 6.5 to 7 points, taken at the weaker end.

## Against what happened

| | Model, Hershey +6.5%, Mars +10.5% | Actual 2025 |
|---|---|---|
| Gross profit | $4.40bn | $4.35bn |
| Gross margin | 37.5% | 37.2% |
| Volume | −1.6% | −1%, reported to the nearest point |

The model was not tuned to 2025. What it leaves out is listed on the
[sources page](https://caspase.ai/hershey/sources/).
