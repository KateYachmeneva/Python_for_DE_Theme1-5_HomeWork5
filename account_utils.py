import json
import os

import numpy as np
import pandas as pd


def _load_table(path: str) -> pd.DataFrame:
    ext = os.path.splitext(path)[1].lower()
    if ext in (".json", ".jsonl"):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return pd.DataFrame(data)
    if ext in (".csv", ".tsv"):
        return pd.read_csv(path)
    raise ValueError(f"Unsupported file extension: {ext}")


def _normalize_and_filter_base(
    df: pd.DataFrame, account_number: str, holder: str | None, account_type: str | None
) -> pd.DataFrame:
    df = df.copy()

    df.rename(columns=str.lower, inplace=True)
    df.rename(
        columns={"date": "date_time", "operation": "operation_type"}, inplace=True
    )

    if "account_number" in df.columns:
        df = df[df["account_number"] == account_number]

    if account_type and "account_type" in df.columns:
        df = df[df["account_type"].astype(str).str.lower() == account_type]
    return df


def _clean_common(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    for col in ("date_time", "operation_type", "amount"):
        if col not in df.columns:
            df[col] = np.nan

    df["date_time"] = pd.to_datetime(df["date_time"], errors="coerce", dayfirst=True)
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

    if "status" in df.columns:
        df["status"] = df["status"].astype(str).str.lower()
    else:
        df["status"] = "success"

    return df
