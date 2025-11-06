import datetime


class Transaction:
    def __init__(
        self,
        operation_type: str,
        amount: float,
        date_time: datetime.datetime,
        balance_after: float,
        status: str,
    ):
        self.operation_type = operation_type
        self.amount = amount
        self.date_time = date_time
        self.balance_after = balance_after
        self.status = status

    def __repr__(self):
        return (
            f"Transaction(type={self.operation_type}, amount={self.amount}, "
            f"date_time={self.date_time}, balance_after={self.balance_after}, status={self.status})"
        )
