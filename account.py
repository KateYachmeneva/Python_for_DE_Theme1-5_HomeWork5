import datetime
import re

import matplotlib.pyplot as plt
import pandas as pd

from transaction import Transaction


class Account:
    _account_counter = 1000  # Приватный атрибут для количества счетов

    def __init__(self, account_holder: str, balance: float = 0.0):
        if not re.match(
            r"^[А-ЯЁ][а-яё]+ [А-ЯЁ][а-яё]+$|^[A-Z][a-z]+ [A-Z][a-z]+$", account_holder
        ):
            raise ValueError(
                "Имя владельца должно быть в формате 'Имя Фамилия' с заглавных букв, кириллицей или латиницей."
            )

        if balance < 0:
            raise ValueError("Начальный баланс счёта, не может быть отрицательным.")

        self.holder: str = account_holder
        self.account_number: str = f"ACC-{Account._account_counter}"
        Account._account_counter += 1

        self._balance: float = balance
        self.operations_history: list[Transaction] = []

        # Зафиксируем стартовое пополнение (если > 0), чтобы история была полной
        if balance > 0:
            self.record_transaction("deposit", balance, "success")

    def record_transaction(self, operation_type: str, amount: float, status: str):
        transaction = Transaction(
            operation_type=operation_type,
            amount=amount,
            date_time=datetime.datetime.now(),
            balance_after=self._balance,
            status=status,
        )
        self.operations_history.append(transaction)

    def deposit(self, amount: float):
        if amount <= 0:
            raise ValueError("Сумма депозита должна быть положительной.")
        self._balance += amount
        self.record_transaction("deposit", amount, "success")

    def withdraw(self, amount: float):
        if amount <= 0:
            raise ValueError("Сумма снятия должна быть положительной.")
        if amount > self._balance:
            self.record_transaction("withdraw", amount, "fail")
            return False
        self._balance -= amount
        self.record_transaction("withdraw", amount, "success")
        return True

    def get_balance(self) -> float:
        return self._balance

    def get_history(self) -> list[Transaction]:
        return self.operations_history

    def __repr__(self) -> str:
        return f"<Account {self.account_number} holder={self.holder!r} balance={self._balance:.2f}>"

    def plot_history(self):
        # Создание датафрейма на основе истории операций
        df = pd.DataFrame(
            [
                {
                    "date_time": t.date_time.strftime("%d.%m %H:%M:%S"),
                    "balance_after": t.balance_after,
                }
                for t in self.operations_history
            ]
        )
        plt.figure(figsize=(10, 5))
        plt.plot(df["date_time"], df["balance_after"], marker="o", linestyle="-")

        plt.title("Изменение баланса счета")
        plt.xlabel("Дата и время операции")
        plt.ylabel("Баланс после операции")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def analyze_transactions(self, n):
        sorted_ops = sorted(
            self.operations_history, key=lambda x: (x.amount, x.date_time), reverse=True
        )
        return sorted_ops[:n]
