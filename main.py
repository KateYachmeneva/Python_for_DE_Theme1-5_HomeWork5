from datetime import timedelta

from account import Account
from savings_account import SavingsAccount


def main():
    acc = Account("Екатерина Ячменева", 1000)

    # делаем операции с шагом в минуту
    acc.deposit(500)
    acc.operations_history[-1].date_time += timedelta(minutes=1)

    acc.withdraw(300)
    acc.operations_history[-1].date_time += timedelta(minutes=2)

    acc.withdraw(2000)
    acc.operations_history[-1].date_time += timedelta(minutes=3)

    acc.deposit(200)
    acc.operations_history[-1].date_time += timedelta(minutes=4)

    print("История операций:")
    for t in acc.get_history():
        print(
            f"{t.date_time:%d.%m %H:%M:%S} | {t.operation_type:<8} | "
            f"{t.amount:<8.2f} | {t.status:<7} | Баланс: {t.balance_after:.2f}"
        )

    # визуализация истории
    acc.plot_history()

    try:
        acc.deposit(200)
        acc.deposit(-100)
    except ValueError as e:
        print("Ошибка при депозите:", e)

    try:
        acc.withdraw(200)
        acc.withdraw(-50)
    except ValueError as e:
        print("Ошибка при снятии:", e)

    print(acc.analyze_transactions(2))

    s = SavingsAccount("Иван Иванов", 1000)
    print(s.apply_interest(5))
    print(s.withdraw(600))  # должно быть False


if __name__ == "__main__":
    main()
