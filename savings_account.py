from __future__ import annotations

from datetime import datetime
from typing import Tuple

import pandas as pd

from account import Account
from account_utils import _clean_common, _load_table, _normalize_and_filter_base


class SavingsAccount(Account):
    account_type = "savings"
    ALLOWED_OPS = {"deposit", "withdraw", "interest"}

    def apply_interest(self, rate: float):
        if rate < 0:
            raise ValueError("Процентная ставка не может быть отрицательной.")
        interest = self._balance * rate / 100
        self._balance += interest
        self.record_transaction("Начисление процентов", interest, "success")

    def withdraw(self, amount: float):
        if amount <= 0:
            raise ValueError("Сумма снятия должна быть положительной.")
        limit = self._balance * 0.5
        if amount > limit:
            self.record_transaction("withdraw", amount, "fail")
            return False

        # Делегируем успешное снятие базовому класс
        return super().withdraw(amount)

    def clean_history(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
        df = _clean_common(df)

        mask_ops = df["operation_type"].isin(self.ALLOWED_OPS)
        mask_amt = df["amount"] > 0
        mask_dt = df["date_time"].notna()
        now = pd.Timestamp.now()
        mask_future = df["date_time"] <= now + pd.Timedelta(days=365 * 5)

        ok = mask_ops & mask_amt & mask_dt & mask_future

        errors = df.loc[~ok, ["date_time", "operation_type", "amount", "status"]].copy()

        def reason(i):
            if not mask_ops.loc[i]:
                return "invalid_operation"
            if not mask_amt.loc[i]:
                return "non_positive_amount"
            if not mask_dt.loc[i]:
                return "invalid_datetime"
            if not mask_future.loc[i]:
                return "datetime_in_future"
            return "unknown"

        if not errors.empty:
            errors["reason"] = [reason(i) for i in errors.index]

        clean = (
            df.loc[ok, ["date_time", "operation_type", "amount", "status"]]
            .sort_values("date_time")
            .reset_index(drop=True)
        )
        return clean, errors

    def load_history_from_file(self, path: str) -> dict:
        raw = _load_table(path)
        # Фильтруем по номеру счёта/владельцу и типу "savings"
        df = _normalize_and_filter_base(
            raw, self.account_number, getattr(self, "holder", None), self.account_type
        )
        print(df)
        if df.empty:
            return {"applied": 0, "skipped": 0, "errors_df": pd.DataFrame()}

        clean, errors = self.clean_history(df)
        applied = 0

        for _, row in clean.iterrows():
            op = row["operation_type"]
            amt = float(row["amount"])
            ts: datetime = row["date_time"].to_pydatetime()
            status = row["status"]

            if op == "deposit":
                self.deposit(amt)
                self.operations_history[-1].date_time = ts

            elif op == "withdraw":
                if status == "fail":
                    self.record_transaction("withdraw", amt, "fail")
                    self.operations_history[-1].date_time = ts
                else:
                    self.withdraw(amt)
                    self.operations_history[-1].date_time = ts

            elif op == "interest":
                self.apply_interest(amt)
                self.operations_history[-1].date_time = ts

            applied += 1

        return {"applied": applied, "skipped": len(errors), "errors_df": errors}
