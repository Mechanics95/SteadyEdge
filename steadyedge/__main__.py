"""CLI.

    python -m steadyedge download --config configs/us_sleeves.yaml
    python -m steadyedge run --config configs/us_sleeves.yaml
    python -m steadyedge run --config configs/us_sleeves.yaml --final-holdout   # one shot only
"""
import argparse
import json

from . import data as D
from .experiment import load_config, run_config


def main() -> None:
    p = argparse.ArgumentParser(prog="steadyedge")
    sub = p.add_subparsers(dest="cmd", required=True)
    for c in ("download", "run"):
        s = sub.add_parser(c)
        s.add_argument("--config", required=True)
        if c == "run":
            s.add_argument("--final-holdout", action="store_true",
                           help="open the sealed holdout period (allowed once per holdout)")
    a = p.parse_args()
    cfg = load_config(a.config)
    if a.cmd == "download":
        D.download(sorted(set(cfg["universe"]) | {cfg["benchmark"]}), cfg["market"], cfg.get("download_start", "2005-01-01"))
    else:
        out = run_config(cfg, use_holdout=a.final_holdout)
        print(json.dumps(out["metrics"], indent=2))
        print(f"report: results/{cfg['name']}/report.md")


if __name__ == "__main__":
    main()
