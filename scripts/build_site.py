"""Build the public results dashboard (site/index.html) from results/.

    python scripts/build_site.py

Self-contained HTML: data is embedded, charts are drawn with inline SVG + JS,
no external requests.
"""
from __future__ import annotations

import html
import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
SITE = ROOT / "site"

def discover() -> list[tuple[str, str, str]]:
    """Every non-synthetic experiment in results/, US first, then by name."""
    out = []
    for d in sorted(RESULTS.glob("*/run_meta.json")):
        cfg = json.loads(d.read_text())["config"]
        if cfg.get("data") == "synthetic":
            continue
        cur = "$" if cfg["market"] == "us" else "Rs "
        out.append((d.parent.name, cfg.get("title", d.parent.name), cur, cfg["market"]))
    out.sort(key=lambda x: (x[3] != "us", x[1]))
    return [(a, b, c) for a, b, c, _ in out]
CHART_SERIES = [("benchmark_buy_hold", "Index (buy and hold)"),
                ("active_only", "Active sleeve only"),
                ("blend_fixed_80", "Blend 80% stable / 20% active")]
LABELS = {
    "benchmark_buy_hold": "Index, buy and hold (benchmark)",
    "stable_only": "Stable sleeve only",
    "active_only": "Active sleeve only",
    "blend_fixed_90": "Blend 90/10", "blend_fixed_80": "Blend 80/20", "blend_fixed_70": "Blend 70/30",
    "blend_fixed_60": "Blend 60/40", "blend_fixed_50": "Blend 50/50",
    "blend_vol_target": "Blend, volatility target", "blend_drawdown_throttle": "Blend, drawdown throttle",
}


def pct(x):
    return "" if x is None or x != x else f"{x * 100:.1f}%"


def gate(m: dict) -> list[tuple[str, bool]]:
    return [
        ("Beats index after costs", (m.get("excess_cagr") or 0) > 0),
        ("Edge over index is statistically real (Deflated Sharpe of excess return > 0.95)", (m.get("dsr_vs_index") or 0) > 0.95),
        ("Max drawdown better than -25%", m["max_drawdown"] > -0.25),
        ("Kill switch never fired", m.get("killed_on") in (None, "None")),
    ]


def market_section(name: str, title: str, cur: str) -> tuple[str, dict]:
    d = RESULTS / name
    if not (d / "metrics.json").exists():
        return f"<section><h2>{title}</h2><p class='muted'>No results yet.</p></section>", {}
    metrics = json.loads((d / "metrics.json").read_text())
    meta = json.loads((d / "run_meta.json").read_text())
    eq = pd.read_csv(d / "equity.csv", index_col=0, parse_dates=True)
    eqw = eq.resample("W-FRI").last().dropna(how="all")
    chart = {"dates": [str(x.date()) for x in eqw.index],
             "series": [{"name": lab, "values": [round(v, 2) for v in eqw[k].tolist()]}
                        for k, lab in CHART_SERIES if k in eqw],
             "cur": cur}
    cap = meta["config"]["capital"]

    rows = []
    for k, m in metrics.items():
        rows.append(
            f"<tr><td>{html.escape(LABELS.get(k, k))}</td><td>{cur}{m['final_equity']:,.0f}</td>"
            f"<td>{pct(m['cagr'])}</td><td>{pct(m['max_drawdown'])}</td><td>{pct(m['worst_12m'])}</td>"
            f"<td>{m['sharpe']:.2f}</td><td>{'' if m.get('dsr_vs_index') is None else f"{m['dsr_vs_index']:.2f}"}</td><td>{pct(m.get('excess_cagr'))}</td>"
            f"<td>{pct(m['cost_drag_pct_of_capital_per_year'])}</td><td>{m['killed_on'] or ''}</td></tr>")

    best_k = max((k for k in metrics if k not in ("benchmark_buy_hold", "stable_only")), key=lambda k: metrics[k]["sharpe"])
    g = gate(metrics[best_k])
    gate_html = "".join(f"<li class='{'pass' if ok else 'fail'}'><span aria-hidden='true'>{'✓' if ok else '✗'}</span> "
                        f"{html.escape(t)} <span class='muted'>({'pass' if ok else 'fail'})</span></li>" for t, ok in g)
    verdict = "passes" if all(ok for _, ok in g) else "does not pass"

    trades_html = ""
    tp = d / "trades.csv"
    if tp.exists():
        t = pd.read_csv(tp)
        t = t[t["variant"] == "active_only"].tail(25).iloc[::-1]
        trades_html = "".join(
            f"<tr><td>{r.date[:10]}</td><td>{html.escape(r.ticker)}</td><td>{r.side}</td>"
            f"<td>{r.shares:.3g}</td><td>{cur}{r.price:,.2f}</td><td>{cur}{r.cost:,.2f}</td></tr>"
            for r in t.itertuples())

    folds = "".join(f"<tr><td>{f['test']}</td><td><code>{html.escape(json.dumps(f['chosen']))}</code></td></tr>"
                    for f in meta["walk_forward_folds"])
    fixes = "".join(f"<li>{html.escape(x)}</li>" for x in meta.get("data_fixes", [])) or "<li>none</li>"
    bias = "<p class='note'>Known bias: the India stock list is today's large caps, so history is " \
           "survivorship-biased upward. Treat active-sleeve results as optimistic.</p>" if "india" in name else ""

    sec = f"""
<section>
  <h2 id="{name}">{html.escape(title)}</h2>
  <p class="muted">Out-of-sample window {meta['oos_start']} to {meta['data_end']} · starting capital {cur}{cap:,} ·
  run <code>{meta['run_id']}</code> · commit <code>{meta['git_commit']}</code> · {metrics[best_k]['n_trials_family']} trials counted for this market</p>
  {bias}
  <h3>Growth of {cur}{cap:,}</h3>
  <div class="chart" id="chart-{name}" role="img" aria-label="Growth of capital, {title}"></div>
  <h3>Promotion gate: best variant ({html.escape(LABELS.get(best_k, best_k))}) {verdict}</h3>
  <ul class="gate">{gate_html}</ul>
  <h3>All variants</h3>
  <div class="scroll"><table>
    <thead><tr><th>Variant</th><th>Ending value</th><th>CAGR</th><th>Max drawdown</th><th>Worst 12 months</th>
    <th>Sharpe</th><th>Edge confidence</th><th>vs index / yr</th><th>Costs / yr</th><th>Kill switch</th></tr></thead>
    <tbody>{''.join(rows)}</tbody></table></div>
  <details><summary>Latest active-sleeve trades (simulated)</summary>
    <div class="scroll"><table><thead><tr><th>Date</th><th>Ticker</th><th>Side</th><th>Shares</th><th>Price</th><th>Cost</th></tr></thead>
    <tbody>{trades_html}</tbody></table></div></details>
  <details><summary>Walk-forward parameter choices</summary>
    <table><thead><tr><th>Test year</th><th>Chosen settings</th></tr></thead><tbody>{folds}</tbody></table></details>
  <details><summary>Data fixes applied</summary><ul>{fixes}</ul></details>
</section>"""
    return sec, chart


PAGE = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>SteadyEdge research results</title>
<style>
.viz-root{color-scheme:light;--surface-1:#ffffff;--surface-2:#f6f6f4;--text-primary:#191919;--text-secondary:#666666;
--grid:#e6e6e6;--series-1:#257de0;--series-2:#f47230;--series-3:#00b894;--good:#008a17;--bad:#c62828}
@media (prefers-color-scheme: dark){.viz-root{color-scheme:dark;--surface-1:#191919;--surface-2:#222;--text-primary:#efefef;
--text-secondary:#9c9c9c;--grid:#333;--series-1:#338ced;--series-2:#e76624;--series-3:#00a888;--good:#0aac23;--bad:#eb6263}}
body{margin:0}
.viz-root{background:var(--surface-1);color:var(--text-primary);font:15px/1.5 system-ui,-apple-system,Segoe UI,sans-serif;min-height:100vh}
main{max-width:1000px;margin:0 auto;padding:24px 20px 60px}
h1{margin:0 0 4px;font-size:28px}h2{margin-top:44px;border-top:1px solid var(--grid);padding-top:24px}h3{font-size:16px;margin:24px 0 8px}
.muted{color:var(--text-secondary);font-size:13px}.note{background:var(--surface-2);padding:10px 14px;border-radius:8px;font-size:14px}
.disclaimer{background:var(--surface-2);border-left:4px solid var(--series-2);padding:12px 16px;border-radius:6px;font-size:14px}
table{border-collapse:collapse;width:100%;font-size:13px;font-variant-numeric:tabular-nums}
th,td{text-align:right;padding:6px 8px;border-bottom:1px solid var(--grid);white-space:nowrap}th:first-child,td:first-child{text-align:left}
th{color:var(--text-secondary);font-weight:600}.scroll{overflow-x:auto}
.gate{list-style:none;padding:0}.gate li{padding:2px 0}.gate .pass span[aria-hidden]{color:var(--good)}.gate .fail span[aria-hidden]{color:var(--bad)}
details{margin:12px 0}summary{cursor:pointer;color:var(--text-secondary)}
.chart{position:relative;height:320px}.chart svg{width:100%;height:100%;overflow:visible}
.legend{display:flex;gap:16px;flex-wrap:wrap;font-size:13px;margin-bottom:6px}.legend i{display:inline-block;width:14px;height:3px;border-radius:2px;vertical-align:middle;margin-right:6px}
.tip{position:absolute;pointer-events:none;background:var(--surface-1);border:1px solid var(--grid);border-radius:6px;padding:6px 10px;font-size:12px;
box-shadow:0 2px 8px rgba(0,0,0,.12);display:none;white-space:nowrap}
code{font-size:12px}nav{margin-top:18px;font-size:14px;line-height:1.9}a{color:var(--series-1)}
</style></head>
<body class="viz-root"><main>
<h1>SteadyEdge</h1>
<p class="muted">Research-first backtests for US and Indian equities: a stable index sleeve, an active momentum sleeve,
and the split between them. Updated __UPDATED__.</p>
<div class="disclaimer"><strong>Not financial advice.</strong> These are simulations on past data with modelled costs.
Backtests usually look better than live trading and do not guarantee future results. Only out-of-sample (walk-forward)
results are shown, and every variant ever tried is counted in the Deflated Sharpe Ratio.</div>
__TOC__
__SECTIONS__
<h2>How it works</h2>
<p>Each evening the strategy decides what to hold; trades fill at the next morning's open with modelled fees and slippage.
The active sleeve's settings are chosen each year using only earlier data. A model is considered for paper trading only if
it passes the promotion gate. Code, tests and the decision log are in the
<a href="https://github.com/Mechanics95/SteadyEdge">repository</a>.</p>
</main>
<script>
const DATA = __DATA__;
const COLORS = ['var(--series-1)','var(--series-2)','var(--series-3)'];
function fmt(cur,v){return cur+Math.round(v).toLocaleString();}
function draw(id, c){
  const el=document.getElementById(id); if(!el) return;
  const W=el.clientWidth||900,H=300,m={l:64,r:16,t:8,b:28};
  const n=c.dates.length, all=c.series.flatMap(s=>s.values).filter(v=>v!=null);
  let lo=Math.min(...all),hi=Math.max(...all); const pad=(hi-lo)*0.05; lo-=pad; hi+=pad;
  const x=i=>m.l+(W-m.l-m.r)*i/(n-1), y=v=>m.t+(H-m.t-m.b)*(1-(v-lo)/(hi-lo));
  const ns='http://www.w3.org/2000/svg';
  const leg=document.createElement('div'); leg.className='legend';
  c.series.forEach((s,k)=>{leg.innerHTML+=`<span><i style="background:${COLORS[k]}"></i>${s.name}</span>`});
  el.before(leg);
  const svg=document.createElementNS(ns,'svg'); svg.setAttribute('viewBox',`0 0 ${W} ${H}`);
  let g='';
  for(let t=0;t<=4;t++){const v=lo+(hi-lo)*t/4;g+=`<line x1="${m.l}" x2="${W-m.r}" y1="${y(v)}" y2="${y(v)}" stroke="var(--grid)"/>`+
    `<text x="${m.l-8}" y="${y(v)+4}" text-anchor="end" font-size="11" fill="var(--text-secondary)">${fmt(c.cur,v)}</text>`;}
  const years=[...new Set(c.dates.map(d=>d.slice(0,4)))];
  years.forEach(yr=>{const i=c.dates.findIndex(d=>d.startsWith(yr)); if(i>0&&+yr%2===0) g+=
    `<text x="${x(i)}" y="${H-8}" text-anchor="middle" font-size="11" fill="var(--text-secondary)">${yr}</text>`;});
  c.series.forEach((s,k)=>{const p=s.values.map((v,i)=>v==null?'':`${i?'L':'M'}${x(i).toFixed(1)},${y(v).toFixed(1)}`).join('');
    g+=`<path d="${p}" fill="none" stroke="${COLORS[k]}" stroke-width="2" stroke-linejoin="round"/>`;});
  g+=`<line id="${id}-x" y1="${m.t}" y2="${H-m.b}" stroke="var(--text-secondary)" stroke-dasharray="3 3" visibility="hidden"/>`;
  c.series.forEach((s,k)=>{g+=`<circle id="${id}-d${k}" r="4" fill="${COLORS[k]}" stroke="var(--surface-1)" stroke-width="2" visibility="hidden"/>`;});
  g+=`<rect x="${m.l}" y="0" width="${W-m.l-m.r}" height="${H}" fill="transparent"/>`;
  svg.innerHTML=g; el.appendChild(svg);
  const tip=document.createElement('div'); tip.className='tip'; el.appendChild(tip);
  svg.addEventListener('mousemove',e=>{
    const r=svg.getBoundingClientRect(), px=(e.clientX-r.left)*W/r.width;
    const i=Math.max(0,Math.min(n-1,Math.round((px-m.l)/(W-m.l-m.r)*(n-1))));
    const xl=svg.querySelector(`#${CSS.escape(id)}-x`); xl.setAttribute('x1',x(i)); xl.setAttribute('x2',x(i)); xl.setAttribute('visibility','visible');
    let h=`<strong>${c.dates[i]}</strong>`;
    c.series.forEach((s,k)=>{const d=svg.querySelector(`#${CSS.escape(id)}-d${k}`); const v=s.values[i];
      if(v!=null){d.setAttribute('cx',x(i));d.setAttribute('cy',y(v));d.setAttribute('visibility','visible');
      h+=`<br><i style="display:inline-block;width:10px;height:3px;background:${COLORS[k]};vertical-align:middle;margin-right:6px"></i>${s.name}: ${fmt(c.cur,v)}`;}});
    tip.innerHTML=h; tip.style.display='block';
    const tx=x(i)*r.width/W; tip.style.left=(tx>r.width*0.6?tx-tip.offsetWidth-12:tx+12)+'px'; tip.style.top='8px';
  });
  svg.addEventListener('mouseleave',()=>{tip.style.display='none';svg.querySelectorAll('[visibility]').forEach(n=>n.setAttribute('visibility','hidden'));});
}
for(const [id,c] of Object.entries(DATA)) draw('chart-'+id,c);
</script></body></html>"""


def paper_section() -> tuple[str, dict]:
    root = ROOT / "paper"
    parts, data = [], {}
    for m, title, cur in (("us", "United States", "$"), ("india", "India", "Rs ")):
        meta_p = root / m / "paper_meta.json"
        if not meta_p.exists():
            continue
        meta = json.loads(meta_p.read_text())
        last = meta["last_run"]
        led = pd.read_csv(root / m / "ledger.csv", index_col=0, parse_dates=True)
        data[f"paper-{m}"] = {"dates": [str(x.date()) for x in led.index], "cur": cur, "series": [
            {"name": "Index (buy and hold)", "values": led["index_hold"].round(2).tolist()},
            {"name": "SteadyEdge v2 80/20 (paper)", "values": led["equity"].round(2).tolist()}]}
        pos = pd.read_csv(root / m / "positions.csv", index_col=0)
        pos_html = "".join(f"<tr><td>{html.escape(str(t))}</td><td>{r.shares:.4g}</td><td>{cur}{r.value:,.2f}</td></tr>"
                           for t, r in pos.iterrows()) or "<tr><td colspan=3>cash only</td></tr>"
        parts.append(f"""
  <h3>{title}: {cur}{last['equity']:,.2f} ({last['return_since_start']:+.2%})
  vs index {cur}{last['index_hold']:,.2f} ({last['index_return_since_start']:+.2%})</h3>
  <p class="muted">Started {meta['start']} with {cur}{meta['capital']:,} · last update {last['date']} ·
  latest decision: {last['action']}{' · KILL SWITCH FIRED ' + last['killed_on'] if last.get('killed_on') else ''}</p>
  <div class="chart" id="chart-paper-{m}" role="img" aria-label="Paper trading equity, {title}"></div>
  <details><summary>Current positions</summary><table><thead><tr><th>Ticker</th><th>Shares</th><th>Value</th></tr></thead>
  <tbody>{pos_html}</tbody></table></details>""")
    if not parts:
        return "", {}
    return ("<section><h2 id='paper'>Paper trading (live forward test, simulated)</h2>"
            "<p>Every trading day the strategy's decision is frozen in the repository before the next day's "
            "prices exist, then replayed with the same costs. No real money and no broker. "
            "Daily notes are in <code>paper/&lt;market&gt;/journal.md</code>.</p>" + "".join(parts) + "</section>"), data


def main() -> None:
    psec, data = paper_section()
    sections = [psec] if psec else []
    for name, title, cur in discover():
        s, c = market_section(name, title, cur)
        sections.append(s)
        if c:
            data[name] = c
    updated = pd.Timestamp.now(tz="UTC").strftime("%Y-%m-%d %H:%M UTC")
    toc = "<nav><a href='#paper'>Paper trading</a> · <strong>Experiments:</strong> " + " · ".join(
        f"<a href='#{n}'>{html.escape(t)}</a>" for n, t, _ in discover()) + "</nav>"
    page = PAGE.replace("__TOC__", toc).replace("__SECTIONS__", "\n".join(sections)) \
               .replace("__DATA__", json.dumps(data)).replace("__UPDATED__", updated)
    SITE.mkdir(exist_ok=True)
    (SITE / "index.html").write_text(page)
    print(f"wrote {SITE / 'index.html'} ({len(page) // 1024} KB)", file=sys.stderr)


if __name__ == "__main__":
    main()
