from account import Account


class SavingsAccount(Account):
    account_type = "Сберегательный счет"

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
