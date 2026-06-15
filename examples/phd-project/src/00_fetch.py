"""Fetch the raw data into data/raw/, then freeze each file read-only.

Provenance — where every raw file comes from. Run this once; afterwards the
raw data is immutable evidence and is never edited by hand.

  * F-F_Research_Data_Factors.csv, 10_Industry_Portfolios.csv
        Kenneth R. French Data Library, Tuck School of Business at Dartmouth.
        Built from CRSP. Free for research use — fetched here, not
        redistributed in this repo (hence data/raw/ is git-ignored).
  * USREC.csv
        NBER recession indicator via FRED, Federal Reserve Bank of St. Louis.
        Public domain.
"""

import io
import stat
import zipfile
from pathlib import Path
from urllib.request import Request, urlopen

RAW = Path(__file__).resolve().parents[1] / "data" / "raw"

# name in data/raw  ->  (kind, url)
SOURCES = {
    "F-F_Research_Data_Factors.csv": (
        "zip",
        "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_Factors_CSV.zip",
    ),
    "10_Industry_Portfolios.csv": (
        "zip",
        "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/10_Industry_Portfolios_CSV.zip",
    ),
    "USREC.csv": (
        "csv",
        "https://fred.stlouisfed.org/graph/fredgraph.csv?id=USREC",
    ),
}

READ_ONLY = stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH


def _download(url: str) -> bytes:
    req = Request(url, headers={"User-Agent": "phd-project-example/1.0"})
    with urlopen(req) as resp:
        return resp.read()


def main() -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    for name, (kind, url) in SOURCES.items():
        dest = RAW / name
        if dest.exists():
            print(f"skip  {name} (already present)")
            continue
        print(f"fetch {name}")
        blob = _download(url)
        if kind == "zip":
            with zipfile.ZipFile(io.BytesIO(blob)) as z:
                inner = next(n for n in z.namelist() if n.lower().endswith(".csv"))
                blob = z.read(inner)
        dest.write_bytes(blob)
        dest.chmod(READ_ONLY)  # freeze: raw is immutable


if __name__ == "__main__":
    main()
