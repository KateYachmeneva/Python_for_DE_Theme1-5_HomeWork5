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

    account_save = SavingsAccount("Иван Иванов", 1000)
    print(account_save.apply_interest(5))
    print(account_save.withdraw(600))
    account_save.account_number = "ACC-100004"  # чтобы совпадало с номером в файле

    # 1. пробуем загрузить историю из файла (поддерживает JSON и CSV)
    result = account_save.load_history_from_file("transactions_dirty.json")

    # 2. выводим результаты проверки
    print("Загрузка завершена.")
    print(f"Применено операций: {result['applied']}")
    print(f"Пропущено (ошибочных): {result['skipped']}")

    if not result["errors_df"].empty:
        print("\nНайдены ошибки в данных:")
        print(result["errors_df"][["date_time", "operation_type", "amount", "reason"]])

    # 3. выводим обновлённый баланс и историю
    print(f"\nТекущий баланс: {account_save.get_balance():.2f}")
    print("\nИстория операций:")
    for t in account_save.get_history():
        print(
            f"{t.date_time:%d.%m %H:%M:%S} | {t.operation_type:<8} | "
            f"{t.amount:<8.2f} | {t.status:<7} | Баланс: {t.balance_after:.2f}"
        )

    # 4. визуализация истории
    account_save.plot_history()

    result = account_save.load_history_from_file("transactions_dirty.csv")
    print("Загрузка завершена.")
    print(f"Применено операций: {result['applied']}")
    print(f"Пропущено (ошибочных): {result['skipped']}")

    if not result["errors_df"].empty:
        print("\nНайдены фошибки в данных:")
        print(result["errors_df"][["date_time", "operation_type", "amount", "reason"]])

    print(f"\nТекущий баланс: {account_save.get_balance():.2f}")
    print("\nИстория операций:")
    for t in account_save.get_history():
        print(
            f"{t.date_time:%d.%m %H:%M:%S} | {t.operation_type:<8} | "
            f"{t.amount:<8.2f} | {t.status:<7} | Баланс: {t.balance_after:.2f}"
        )

    account_save.plot_history()

    account_check = SavingsAccount("Катя Ячменева")
    account_check.account_number = "ACC-100004"  # чтобы совпадало с номером в файле

    # 1. пробуем загрузить историю из файла (поддерживает JSON и CSV)

    result = account_check.load_history_from_file("transactions_dirty.json")

    # 2. выводим результаты проверки
    print("Загрузка завершена.")
    print(f"Применено операций: {result['applied']}")
    print(f"Пропущено (ошибочных): {result['skipped']}")

    if not result["errors_df"].empty:
        print("\nНайдены ошибки в данных:")
        print(result["errors_df"][["date_time", "operation_type", "amount", "reason"]])

    # 3. выводим обновлённый баланс и историю
    print(f"\nТекущий баланс: {account_check.get_balance():.2f}")
    print("\nИстория операций:")
    for t in account_check.get_history():
        print(
            f"{t.date_time:%d.%m %H:%M:%S} | {t.operation_type:<8} | "
            f"{t.amount:<8.2f} | {t.status:<7} | Баланс: {t.balance_after:.2f}"
        )

    # 4. визуализация истории
    account_check.plot_history()

    result = account_check.load_history_from_file("transactions_dirty.csv")
    print("Загрузка завершена.")
    print(f"Применено операций: {result['applied']}")
    print(f"Пропущено (ошибочных): {result['skipped']}")

    if not result["errors_df"].empty:
        print("\nНайдены ошибки в данных:")
        print(result["errors_df"][["date_time", "operation_type", "amount", "reason"]])

    print(f"\nТекущий баланс: {account_check.get_balance():.2f}")
    print("\nИстория операций:")
    for t in account_check.get_history():
        print(
            f"{t.date_time:%d.%m %H:%M:%S} | {t.operation_type:<8} | "
            f"{t.amount:<8.2f} | {t.status:<7} | Баланс: {t.balance_after:.2f}"
        )

    account_check.plot_history()


if __name__ == "__main__":
    main()
