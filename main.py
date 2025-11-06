from datetime import timedelta

from account import Account


def main():
    acc = Account("Екатерина", 1000)

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


if __name__ == "__main__":
    main()
