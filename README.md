# Brandenburg

The code behind *The RGM Files*, a weekly case study in revenue growth
management: the work of deciding what a consumer-goods company charges, which
pack sizes it sells, when it promotes and what it agrees with retailers.

Each episode takes one real decision by a well-known food, drink or household
brand. It sets out what the company did and what happened, in public numbers
with a source for every one, then says what we would have recommended instead.
The model in each episode lets you change the inputs and see whether you would
have called it differently.

## Run it

```
pip install -r requirements.txt
streamlit run episodes/01-list-price/app.py    # one episode
streamlit run app.py                           # all of them
```

## What each episode folder holds

- `README.md`: the case, what the company did, the results, what we would have
  done differently, and a verification checklist that gives a source and a date
  for every number.
- `app.py`: the model.
- `data/`: its inputs. Each file says where it came from.

A number that has not been checked against a source is labelled
`ILLUSTRATIVE — verify before publishing`, in the app and in the code. Nothing
labelled that way is posted.

## Episodes

| # | topic | case | posted |
|---|---|---|---|

The live versions run at caspase.ai.

## Licence

MIT. Fork it, change it, use it. See `LICENSE`.
