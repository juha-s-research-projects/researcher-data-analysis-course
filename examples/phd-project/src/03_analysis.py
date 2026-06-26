"""The analysis: does each industry move with the market, and does that change
in recessions?

For every industry we run one regression on the tidy panel built by 02_clean:

    (industry return - risk-free) ~ market factor + recession dummy

The coefficient on the market factor is the industry's *beta* — how much it
amplifies (>1) or dampens (<1) market moves. The recession dummy is a control:
it lets the average return differ in NBER recession months so the beta isn't
distorted by them.

Outputs are written fresh every run, so they are never edited by hand:
  * outputs/tables/industry_betas.tex  — a LaTeX table, ready for the paper
  * outputs/figures/industry_betas.pdf — betas as a bar chart
Re-run this (or run.sh / run.ps1) after any change and both are rebuilt.
"""

import sqlite3
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # write files, never open a window — works on a headless CI

import matplotlib.pyplot as plt  # noqa: E402  (must follow the backend choice)
import pandas as pd  # noqa: E402
import statsmodels.formula.api as smf  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "project.sqlite"
TABLES = ROOT / "outputs" / "tables"
FIGURES = ROOT / "outputs" / "figures"


def _to_latex(df: pd.DataFrame) -> str:
    """Hand-roll a small LaTeX table — keeps the example's deps to a minimum
    (pandas' own to_latex now pulls in jinja2, which we don't otherwise need)."""
    header = " & ".join(c.replace("_", r"\_") for c in df.columns) + r" \\"
    body = "\n".join(
        " & ".join(f"{v:.3f}" if isinstance(v, float) else str(v) for v in row) + r" \\"
        for row in df.itertuples(index=False)
    )
    return (
        "\\begin{table}[ht]\n\\centering\n"
        f"\\begin{{tabular}}{{{'l' + 'r' * (len(df.columns) - 1)}}}\n"
        "\\toprule\n"
        f"{header}\n\\midrule\n{body}\n\\bottomrule\n"
        "\\end{tabular}\n"
        "\\caption{Market beta by industry, controlling for NBER recessions.}\n"
        "\\label{tab:industry_betas}\n\\end{table}\n"
    )


def main() -> None:
    con = sqlite3.connect(DB)
    panel = pd.read_sql("SELECT * FROM panel", con)
    con.close()

    # The thing we actually explain: return earned above the risk-free rate.
    panel["excess"] = panel["ret"] - panel["rf"]

    rows = []
    for industry, sub in panel.groupby("industry"):
        model = smf.ols("excess ~ mkt_rf + recession", data=sub).fit()
        rows.append({
            "industry": industry,
            "alpha": model.params["Intercept"],
            "beta": model.params["mkt_rf"],
            "recession": model.params["recession"],
            "r_squared": model.rsquared,
            "n": int(model.nobs),
        })

    results = (
        pd.DataFrame(rows)
        .sort_values("beta", ascending=False)
        .reset_index(drop=True)
    )

    TABLES.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)

    (TABLES / "industry_betas.tex").write_text(_to_latex(results))

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.barh(results["industry"], results["beta"], color="#4c72b0")
    ax.axvline(1.0, color="0.4", linestyle="--", linewidth=1)  # beta = 1: moves with the market
    ax.set_xlabel("Market beta")
    ax.set_title("Industry sensitivity to the market")
    ax.invert_yaxis()  # highest beta on top
    fig.tight_layout()
    fig.savefig(FIGURES / "industry_betas.pdf")

    print(f"wrote {TABLES / 'industry_betas.tex'}")
    print(f"wrote {FIGURES / 'industry_betas.pdf'}")
    print(results.to_string(index=False))


if __name__ == "__main__":
    main()
