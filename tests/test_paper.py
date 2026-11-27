import pandas as pd
from steadyedge.data import synthetic
from steadyedge.paper import run_paper

CFG = "configs/synthetic_demo.yaml"


def _cut(b, n):
    return {k: v.iloc[:n] for k, v in b.items()}


def test_paper_freezes_decisions_and_tracks_index(tmp_path):
    b = synthetic(n_assets=6, years=8, seed=2)
    n0 = 1600
    s1 = run_paper("demo", CFG, 0.8, tmp_path, _cut(b, n0))
    assert s1["action"] == "rebalance"                       # day one buys the target
    first = pd.read_csv(tmp_path / "demo" / "decisions.csv", index_col=0)
    for k in range(1, 30):
        s = run_paper("demo", CFG, 0.8, tmp_path, _cut(b, n0 + k))
    dec = pd.read_csv(tmp_path / "demo" / "decisions.csv", index_col=0)
    assert len(dec) == 30
    pd.testing.assert_frame_equal(dec.iloc[:1], first)       # history never rewritten
    # Re-running the same day does not add a row or a journal entry.
    run_paper("demo", CFG, 0.8, tmp_path, _cut(b, n0 + 29))
    assert len(pd.read_csv(tmp_path / "demo" / "decisions.csv")) == 30
    j = (tmp_path / "demo" / "journal.md").read_text()
    assert j.count("\n## ") == 30
    led = pd.read_csv(tmp_path / "demo" / "ledger.csv", index_col=0)
    assert led["equity"].iloc[0] == 500 and len(led) == 30
    assert s["equity"] > 0
