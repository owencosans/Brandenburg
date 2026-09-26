"""Where the switching number comes from.

No published study measures how easily shoppers switch between Hershey and
the rest of the chocolate shelf, so the model's value is fitted: the number
that makes the model reproduce Hershey's own volume in periods before the
decision, when both Hershey and the shelf had raised prices.

Run: python3 fit_switching.py
"""
import math

import model as M

# Each check: Hershey's price change, the whole shelf's price change, and
# Hershey's reported volume change over the same period.
CHECKS = [
    # Hershey North America Confectionery, FY2023: price +9.0 points,
    # volume/mix -1.9 points (Hershey Q4 2023 results, 8 February 2024).
    # Shelf price per unit from Circana, 2023 US chocolate: dollars +5.8%,
    # units -5.4% (reported by FoodNavigator, 25 April 2024).
    ("FY2023, shelf price from Circana", 0.090, 1.058 / 0.946 - 1, -0.019),
    # Q1 2024: "elasticity-related volume declines of approximately 4%" on
    # "price realization of nearly 6%" (Hershey Q1 2024 remarks, 3 May 2024).
    # Shelf price, year on year: BLS CPI candy and chewing gum
    # (CUUR0000SEFR02) +4.98%, or BLS PPI chocolate (WPU02550301) +3.76%.
    ("Q1 2024, shelf price from the CPI", 0.059, 0.0498, -0.040),
    ("Q1 2024, shelf price from the PPI", 0.059, 0.0376, -0.040),
]


def hershey_volume(hershey_move, shelf_move, switching):
    """The model's Hershey volume when the whole shelf's price moved by shelf_move."""
    h, shelf = math.log1p(hershey_move), math.log1p(shelf_move)
    rest = (shelf - M.HERSHEY_SHARE * h) / (1 - M.HERSHEY_SHARE)
    return M.run(hershey_move, math.expm1(rest), switching=switching).volume


def fit(hershey_move, shelf_move, observed, lo=0.0, hi=6.0):
    """The switching value at which the model matches the observed volume."""
    f = lambda s: hershey_volume(hershey_move, shelf_move, s) - observed
    if f(lo) * f(hi) > 0:
        return None
    for _ in range(100):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if f(lo) * f(mid) > 0 else (lo, mid)
    return (lo + hi) / 2


if __name__ == "__main__":
    print(f"Category elasticity {M.CATEGORY_ELASTICITY}, Hershey share {M.HERSHEY_SHARE:.0%}\n")
    for name, h, shelf, observed in CHECKS:
        s = fit(h, shelf, observed)
        at_default = hershey_volume(h, shelf, M.SWITCHING)
        print(f"{name}: observed {observed:+.1%}; fits at switching {s:.2f}; "
              f"at the model's {M.SWITCHING} it gives {at_default:+.1%}")
    print(f"\nThe model uses {M.SWITCHING}, between the fits. Low confidence; the page "
          "lets you move it from 0.25 to 3.5.")
