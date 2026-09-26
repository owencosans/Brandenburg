"""The page and the Python model give the same numbers.

Loads the page in a headless browser and compares its window.HM against
model.py across a grid of inputs. It tests the live page unless HERSHEY_PAGE
names another copy (a URL or a local file). Set CHROME to a browser binary if
Playwright's own isn't installed.
Run: pip install playwright && playwright install chromium && python3 tests/test_parity.py
"""
import itertools, json, os, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import model as M
from playwright.sync_api import sync_playwright

PAGE = os.environ.get("HERSHEY_PAGE", "https://caspase.ai/hershey/")
if "://" not in PAGE:
    PAGE = pathlib.Path(PAGE).resolve().as_uri()
CHROME = os.environ.get("CHROME")

cases = list(itertools.product([-0.05, 0.0, 0.065, 0.15, 0.25], [-0.05, 0.0, 0.065, 0.105, 0.2],
                               [-0.2, -0.5, -1.0], [0.25, 1.25, 3.5]))
with sync_playwright() as p:
    b = p.chromium.launch(**({"executable_path": CHROME} if CHROME else {}))
    pg = b.new_page(); pg.goto(PAGE)
    js = pg.evaluate("""cases => cases.map(c => { const r = HM.run(c[0], c[1], c[2], c[3]);
        return [r.margin, r.volume, r.gross_profit_m, r.from_shelf, r.from_switching,
                HM.goalFloor(c[1], c[2], c[3]), HM.marsBreakeven(c[0], c[2], c[3]), HM.elasticities(c[0], c[1], c[2], c[3]).own, HM.elasticities(c[0], c[1], c[2], c[3]).cross]; })""", cases)
    goal = pg.evaluate("HM.GOAL")
    b.close()

assert abs(goal - M.GOAL_M) < 1e-9
worst = 0.0
for c, j in zip(cases, js):
    r = M.run(*c)
    py = [r.margin, r.volume, r.gross_profit_m, r.from_shelf, r.from_switching,
          M.goal_floor(c[1], c[2], c[3]), M.mars_breakeven(c[0], c[2], c[3]), *M.elasticities(*c)]
    for a, bb in zip(py, j):
        if a is None or bb is None:
            assert a is None and bb is None, (c, py, j)
            continue
        worst = max(worst, abs(a - bb) / max(1.0, abs(a)))
assert worst < 1e-9, worst
print(f"parity ok: {len(cases)} cases, worst relative difference {worst:.1e}")
