"""Hershey's August 2024 price decision: the reference model.

Every number the page at caspase.ai/hershey shows is computed here. The page
runs the same math in the browser, and tests/test_parity.py checks the two
agree.

Sources for every input are in data/sources.csv.
"""

import math
from dataclasses import dataclass

# Fixed inputs (data/sources.csv)
HERSHEY_SHARE = 0.45                  # of US chocolate, IRI dollars, calendar 2022
LOCKED_COST = 1.06 * (1 - 0.372)      # 2025 unit cost as a share of the 2024 price
MARGIN_2024 = 0.433                   # 2024 adjusted gross margin
NET_SALES_2024_M = 11_202.3           # 2024 net sales, $ millions

# The 2025 goal Hershey's guidance implies (February 2025): net sales up at
# least 2%, adjusted gross margin down no more than 700 basis points.
MARGIN_TARGET = MARGIN_2024 - 0.070
GOAL_M = NET_SALES_2024_M * 1.02 * MARGIN_TARGET
VOLUME_PROMISE = -0.005               # "slightly down", read as -0.5%

# Best-estimate shopper numbers (data/sources.csv)
CATEGORY_ELASTICITY = -0.5
SWITCHING = 1.25


@dataclass
class Result:
    margin: float
    volume: float
    gross_profit_m: float
    from_shelf: float        # volume change from people buying less chocolate
    from_switching: float    # volume change from people switching brands


def run(hershey_move, mars_move, category=CATEGORY_ELASTICITY, switching=SWITCHING):
    """Hershey's 2025 margin, volume and gross profit for two price moves."""
    h, m = math.log1p(hershey_move), math.log1p(mars_move)
    shelf = category * (HERSHEY_SHARE * h + (1 - HERSHEY_SHARE) * m)
    a = HERSHEY_SHARE * math.exp(-switching * h)
    b = (1 - HERSHEY_SHARE) * math.exp(-switching * m)
    switch = math.log(a / (a + b) / HERSHEY_SHARE)
    volume = math.expm1(shelf + switch)
    price = 1 + hershey_move
    margin = (price - LOCKED_COST) / price
    return Result(margin, volume, NET_SALES_2024_M * price * (1 + volume) * margin,
                  math.expm1(shelf), math.expm1(switch))


def elasticities(hershey_move=0.0, mars_move=0.0, category=CATEGORY_ELASTICITY,
                 switching=SWITCHING):
    """Own- and cross-price elasticity at the given prices.

    The category part is constant. The switching part depends on Hershey's
    share after the moves, so Hershey grows more price-sensitive as it gets
    dearer. It never grows past category x share + switching: the model has
    no price points where shoppers walk away, which is why it overstates
    what very large increases would earn.
    """
    share_after = HERSHEY_SHARE * (1 + run(hershey_move, mars_move, category, switching).from_switching)
    own = category * HERSHEY_SHARE - switching * (1 - share_after)
    cross = category * (1 - HERSHEY_SHARE) + switching * (1 - share_after)
    return own, cross


def _bisect(f, lo, hi):
    """Smallest x in [lo, hi] with f(x) >= 0, for f rising in x."""
    if f(lo) >= 0:
        return lo
    if f(hi) < 0:
        return None
    for _ in range(80):
        mid = (lo + hi) / 2
        lo, hi = (lo, mid) if f(mid) >= 0 else (mid, hi)
    return hi


def goal_floor(mars_move, category=CATEGORY_ELASTICITY, switching=SWITCHING):
    """The smallest Hershey price move that meets the goal."""
    return _bisect(lambda x: run(x, mars_move, category, switching).gross_profit_m - GOAL_M, -0.2, 0.6)


def mars_breakeven(hershey_move, category=CATEGORY_ELASTICITY, switching=SWITCHING):
    """The lowest Mars price move at which Hershey's move still meets the goal."""
    return _bisect(lambda m: run(hershey_move, m, category, switching).gross_profit_m - GOAL_M, -0.5, 0.5)
