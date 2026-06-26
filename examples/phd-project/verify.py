"""Check that the built database is sane, on any OS.

Run this after the pipeline (00_fetch -> 01_load_raw -> 02_clean). It asserts
the *invariants* that must hold no matter when you fetch the data. It does NOT
hardcode the row count: Kenneth French publishes a new month every month, so
the panel grows over time. What stays true is the shape — 10 industries, one
row per industry-month, ISO dates, returns as decimals, a 0/1 recession flag.

Exits 0 if everything holds, 1 (printing every failure) otherwise. Stdlib only,
so it runs the same on Linux, macOS and Windows with no extra dependencies.
"""

import re
import sqlite3
import sys
from pathlib import Path

DB = Path(__file__).resolve().parent / "data" / "project.sqlite"

ISO_MONTH = re.compile(r"^\d{4}-\d{2}-01$")
N_INDUSTRIES = 10
FIRST_MONTH = "1926-07-01"  # both Fama-French series start here


def main() -> int:
    if not DB.exists():
        print(f"FAIL  database not found: {DB}")
        print("      run the pipeline first (00_fetch, 01_load_raw, 02_clean).")
        return 1

    con = sqlite3.connect(DB)
    failures: list[str] = []

    def check(name: str, ok: bool, detail: str = "") -> None:
        if ok:
            print(f"ok    {name}")
        else:
            failures.append(f"{name}{' — ' + detail if detail else ''}")

    def scalar(sql: str):
        return con.execute(sql).fetchone()[0]

    # 1. Every table the pipeline promises is present.
    tables = {r[0] for r in con.execute(
        "SELECT name FROM sqlite_master WHERE type='table'"
    )}
    expected = {
        "factors_raw", "industry_raw", "recession_raw",  # 01_load_raw
        "factors", "industry_returns", "recession", "panel",  # 02_clean
    }
    missing = expected - tables
    check("all tables exist", not missing, f"missing: {sorted(missing)}")

    if missing:  # nothing else is meaningful without the tables
        con.close()
        _report(failures)
        return 1

    # 2. Tidy long shape: exactly 10 industries, one row per industry-month.
    n_ind = scalar("SELECT count(DISTINCT industry) FROM panel")
    check("10 distinct industries", n_ind == N_INDUSTRIES, f"got {n_ind}")

    n_panel = scalar("SELECT count(*) FROM panel")
    n_months = scalar("SELECT count(DISTINCT month) FROM panel")
    check(
        "panel is months x industries",
        n_panel == n_months * N_INDUSTRIES,
        f"{n_panel} rows != {n_months} months * {N_INDUSTRIES}",
    )

    # 3. The factor join dropped nothing — every industry-month has its factors.
    n_returns = scalar("SELECT count(*) FROM industry_returns")
    check(
        "factor join is complete",
        n_panel == n_returns,
        f"panel {n_panel} != industry_returns {n_returns}",
    )

    # 4. No duplicate (month, industry) keys.
    n_dupe = scalar(
        "SELECT count(*) FROM ("
        "  SELECT month, industry FROM panel"
        "  GROUP BY month, industry HAVING count(*) > 1)"
    )
    check("no duplicate industry-months", n_dupe == 0, f"{n_dupe} duplicated keys")

    # 5. Dates are ISO 'YYYY-MM-01' text, and the series starts where we expect.
    bad_dates = scalar(
        "SELECT count(*) FROM panel WHERE month NOT GLOB '????-??-01'"
    )
    check("all months are ISO YYYY-MM-01", bad_dates == 0, f"{bad_dates} bad")
    first = scalar("SELECT min(month) FROM panel")
    check("series starts 1926-07-01", first == FIRST_MONTH, f"got {first}")
    check("min month matches ISO pattern", bool(ISO_MONTH.match(first)))

    # 6. Returns are decimals, not percent, and the -99.99/-999 sentinels are
    #    gone (mapped to NULL). A surviving sentinel would show as ~ -0.9999.
    worst = scalar("SELECT min(ret) FROM panel WHERE ret IS NOT NULL")
    check(
        "no missing-data sentinel survived",
        worst is None or worst > -0.9998,
        f"min ret = {worst}",
    )
    huge = scalar("SELECT count(*) FROM panel WHERE abs(ret) > 5")
    check("returns look like decimals not percent", huge == 0, f"{huge} |ret|>5")

    # 7. The recession flag is a clean 0/1 with no gaps (inner join + COALESCE).
    bad_rec = scalar("SELECT count(*) FROM panel WHERE recession NOT IN (0, 1)")
    check("recession flag is 0/1", bad_rec == 0, f"{bad_rec} bad")
    null_mkt = scalar("SELECT count(*) FROM panel WHERE mkt_rf IS NULL")
    check("every row has a market factor", null_mkt == 0, f"{null_mkt} null mkt_rf")

    con.close()
    print(f"\npanel: {n_panel} rows, {n_months} months, {n_ind} industries, "
          f"from {first}")
    _report(failures)
    return 1 if failures else 0


def _report(failures: list[str]) -> None:
    if failures:
        print(f"\n{len(failures)} check(s) FAILED:")
        for f in failures:
            print(f"  - {f}")
    else:
        print("\nall checks passed")


if __name__ == "__main__":
    sys.exit(main())
