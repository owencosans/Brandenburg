"""Hershey's August 2024 price decision: the reference model.

Every number the demo page shows is computed here. The page runs the same
math in the browser, and a shared test keeps the two in agreement.

Sources for each default are in data/sources.csv.
"""

import math
from dataclasses import dataclass

# Fixed inputs (see data/sources.csv)
HERSHEY_SHARE = 0.45        # of US chocolate, IRI dollars, calendar 2022
LOCKED_COST = 1.06 * (1 - 0.372)   # 2025 unit cost as a share of the 2024 price
MARGIN_2024 = 0.433         # 2024 adjusted gross margin
NET_SALES_2024_M = 11_202.3 # 2024 net sales, $ millions

# 2025 targets, first issued February 2025
MARGIN_TARGET = MARGIN_2024 - 0.070   # "contract by approximately 650-700 bps"
VOLUME_TARGET = -0.005                # "slightly down", read as -0.5%

# Best-estimate shopper numbers (see data/sources.csv)
CATEGORY_ELASTICITY = -0.5
SWITCHING = 1.25


@dataclass
class Result:
    margin: float
    volume: float
    gross_profit_m: float
    from_shelf: float       # volume change from people buying less chocolate
    from_switching: float   # volume change from people switching brands

    @property
    def hits_margin(self):
        return self.margin >= MARGIN_TARGET

    @property
    def hits_volume(self):
        return self.volume >= VOLUME_TARGET


def run(hershey_move, mars_move, category=CATEGORY_ELASTICITY, switching=SWITCHING,
        share=HERSHEY_SHARE):
    """Hershey's 2025 margin, volume and gross profit for two price moves."""
    h, m = math.log1p(hershey_move), math.log1p(mars_move)
    shelf = category * (share * h + (1 - share) * m)
    a, b = share * math.exp(-switching * h), (1 - share) * math.exp(-switching * m)
    switch = math.log(a / (a + b) / share)
    volume = math.expm1(shelf + switch)
    price = 1 + hershey_move
    margin = (price - LOCKED_COST) / price
    gross_profit = NET_SALES_2024_M * price * (1 + volume) * margin
    return Result(margin, volume, gross_profit, math.expm1(shelf), math.expm1(switch))


def elasticities(category=CATEGORY_ELASTICITY, switching=SWITCHING, share=HERSHEY_SHARE):
    """Own and cross elasticity implied by the two shopper numbers."""
    own = category * share - switching * (1 - share)
    cross = category * (1 - share) + switching * (1 - share)
    return own, cross


def margin_floor():
    """The smallest Hershey price move that meets the margin target."""
    return LOCKED_COST / (1 - MARGIN_TARGET) - 1


def volume_ceiling(mars_move, category=CATEGORY_ELASTICITY, switching=SWITCHING,
                   lo=-0.2, hi=0.5):
    """The largest Hershey price move that meets the volume target."""
    f = lambda x: run(x, mars_move, category, switching).volume - VOLUME_TARGET
    if f(lo) < 0:
        return None
    if f(hi) >= 0:
        return hi
    for _ in range(80):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if f(mid) >= 0 else (lo, mid)
    return lo
