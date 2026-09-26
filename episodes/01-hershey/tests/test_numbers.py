"""Every number the episode publishes, recomputed. Run: python3 tests/test_numbers.py"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import model as M


def near(a, b, tol):
    assert abs(a - b) <= tol, (a, b)


def test_goal():
    near(M.GOAL_M, 4148, 1)                     # "$4.15bn"


def test_what_they_did():
    r = M.run(0.065, 0.105)
    near(r.gross_profit_m, 4400, 1)             # "$4.40bn"
    near(r.gross_profit_m - M.GOAL_M, 252, 1)   # "clears by $252m"
    near(r.margin, 0.375, 0.0005)               # "37.5%"
    near(r.volume, -0.016, 0.0005)              # "-1.6%"
    near(r.from_shelf, -0.041, 0.0005)
    near(r.from_switching, 0.025, 0.0005)


def test_no_increase_and_more():
    near(M.run(0.0, 0.105).gross_profit_m - M.GOAL_M, -253, 1)
    near(M.run(0.15, 0.105).gross_profit_m - M.GOAL_M, 827, 1)


def test_readouts():
    own, cross = M.elasticities()
    near(own, -0.91, 0.005); near(cross, 0.41, 0.005)          # at 2024 prices
    own50, cross50 = M.elasticities(0.50, 0.105)
    near(own50, -1.03, 0.005); near(cross50, 0.53, 0.005)      # Hershey +50%, Mars +10.5%
    near(M.goal_floor(0.105), 0.032, 0.0005)
    near(M.mars_breakeven(0.065), -0.038, 0.0005)


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn(); print("ok", name)
