"""Turn the raw tables into clean, tidy ones.

Every fix is a rule in code, so anyone can see exactly what was done and re-run
it from the untouched raw files:
  * parse the YYYYMM / YYYY-MM-DD dates onto one monthly key (ISO 'YYYY-MM-01'
    text — SQLite has no dedicated date type, and ISO text sorts correctly),
  * convert returns from percent to decimal,
  * map the -99.99 / -999 missing codes to a real NULL,
  * reshape the wide industry table into tidy long form (one row per
    industry-month),
  * join the three sources into one analysis-ready panel.
"""

import sqlite3
from pathlib import Path

import pandas as pd

DB = Path(__file__).resolve().parents[1] / "data" / "project.sqlite"


def main() -> None:
    con = sqlite3.connect(DB)

    # Factors: percent -> decimal, "192607" -> "1926-07-01".
    con.executescript("""
        DROP TABLE IF EXISTS factors;
        CREATE TABLE factors AS
        SELECT
            substr(ym, 1, 4) || '-' || substr(ym, 5, 2) || '-01' AS month,
            CAST(mkt_rf AS REAL) / 100 AS mkt_rf,
            CAST(smb    AS REAL) / 100 AS smb,
            CAST(hml    AS REAL) / 100 AS hml,
            CAST(rf     AS REAL) / 100 AS rf
        FROM factors_raw;
    """)

    # Industries: wide -> tidy long. SQLite has no UNPIVOT, so we reshape with
    # pandas' melt — the canonical wide-to-long tool. Missing codes -> NULL,
    # percent -> decimal.
    wide = pd.read_sql("SELECT * FROM industry_raw", con)
    long = wide.melt(id_vars="ym", var_name="industry", value_name="ret")
    long["ret"] = pd.to_numeric(long["ret"])
    long.loc[long["ret"] <= -99.98, "ret"] = float("nan")  # -99.99 / -999 -> NULL
    long["ret"] = long["ret"] / 100
    long["month"] = long["ym"].str[:4] + "-" + long["ym"].str[4:6] + "-01"
    long[["month", "industry", "ret"]].to_sql(
        "industry_returns", con, if_exists="replace", index=False
    )

    # Recession: "1854-12-01" -> first-of-month text, to match the others.
    con.executescript("""
        DROP TABLE IF EXISTS recession;
        CREATE TABLE recession AS
        SELECT substr(obs_date, 1, 7) || '-01' AS month,
               CAST(recession AS INTEGER)       AS recession
        FROM recession_raw;
    """)

    # One tidy analysis panel: industry returns + factors + recession flag.
    con.executescript("""
        DROP TABLE IF EXISTS panel;
        CREATE TABLE panel AS
        SELECT i.month, i.industry, i.ret,
               f.mkt_rf, f.smb, f.hml, f.rf,
               COALESCE(r.recession, 0) AS recession
        FROM industry_returns i
        JOIN factors   f ON f.month = i.month
        LEFT JOIN recession r ON r.month = i.month;
    """)
    con.commit()

    n = con.execute("SELECT count(*) FROM panel").fetchone()[0]
    print(f"clean tables built; panel has {n} rows")
    con.close()


if __name__ == "__main__":
    main()
