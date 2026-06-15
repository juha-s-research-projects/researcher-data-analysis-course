"""Load the messy raw files into the project database, as faithfully as possible.

This step only gets the data *into* SQLite. It does not fix units, missing
codes, or shape — that is 02_clean.py's job. All we do here is carve the one
rectangular block we want out of each human-formatted file:

  * The Fama-French files have a few lines of preamble, and stack several
    tables in a single file (monthly, then annual; value- then equal-weighted).
  * We keep only the monthly value-weighted block from each.
"""

import re
import sqlite3
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
DB = ROOT / "data" / "project.sqlite"


def read_ff_factors(path: Path) -> pd.DataFrame:
    lines = path.read_text().splitlines()
    # The monthly rows are exactly those whose first field is a 6-digit YYYYMM.
    # The stacked "Annual Factors" block below uses 4-digit years, so filtering
    # on six digits quietly drops it along with all the preamble text.
    rows = [l.split(",") for l in lines if re.match(r"^\s*\d{6}\s*,", l)]
    df = pd.DataFrame(rows, columns=["ym", "mkt_rf", "smb", "hml", "rf"])
    return df.apply(lambda col: col.str.strip())


def read_industries(path: Path) -> pd.DataFrame:
    lines = path.read_text().splitlines()
    start = next(
        i for i, l in enumerate(lines)
        if "Average Value Weighted Returns -- Monthly" in l
    )
    industries = lines[start + 1].strip().strip(",").split(",")  # 10 names
    rows = []
    for l in lines[start + 2:]:
        if not l.strip():
            break  # the first blank line ends the first table
        rows.append(l.split(","))
    df = pd.DataFrame(rows, columns=["ym"] + industries)
    return df.apply(lambda col: col.str.strip())


def read_usrec(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)  # columns: observation_date, USREC
    df.columns = ["obs_date", "recession"]
    return df


def main() -> None:
    factors = read_ff_factors(RAW / "F-F_Research_Data_Factors.csv")
    industries = read_industries(RAW / "10_Industry_Portfolios.csv")
    usrec = read_usrec(RAW / "USREC.csv")

    con = sqlite3.connect(DB)
    factors.to_sql("factors_raw", con, if_exists="replace", index=False)
    industries.to_sql("industry_raw", con, if_exists="replace", index=False)
    usrec.to_sql("recession_raw", con, if_exists="replace", index=False)
    con.commit()
    con.close()

    print(
        f"loaded: factors_raw={len(factors)}, "
        f"industry_raw={len(industries)}, recession_raw={len(usrec)}"
    )


if __name__ == "__main__":
    main()
