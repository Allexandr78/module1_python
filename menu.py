LOW = "1"
MEDIUM = "2"
HIGH = "3"

NEW = "1"
IN_PROGRESS = "2"
COMPLETED = "3"

PRIORITIES = {LOW: "Низкий", MEDIUM: "Средний", HIGH: "Высокий"}

STATUSES = {NEW: "Новая", IN_PROGRESS: "В процессе", COMPLETED: "Завершена"}

FILENAME = "tasks.txt"

def load_tasks() -> dict:
    """Загрузка задач из файла."""
    tasks = {}
    try:
        with open(FILENAME, "r", encoding="utf-8") as file:
            for line in file:
                task_data = line.strip().split("|")
                if len(task_data) != 5:
                    continue
                task_id = int(task_data[0])
                tasks[task_id] = {
                    "title": task_data[1],
                    "description": task_data[2],
                    "priority": task_data[3],
                    "status": task_data[4],
                }
    except FileNotFoundError:
        pass  # Если файл не найден, возвращаем пустой словарь
    return tasks


def save_tasks(tasks: dict) -> None:
    """Сохранение задач в файл."""
    with open(FILENAME, "w", encoding="utf-8") as file:
        for task_id, task in tasks.items():
            task_line = f"{task_id}|{task['title']}|{task['description']}|"
            "{task['priority']}|{task['status']}\n"
            file.write(task_line)


def output_tasks(task_id: int, task_info: dict) -> None:
    """Вывод задач."""
    print(f"\nID задачи: {task_id}")
    print(f"Название: {task_info['title']}")
    print(f"Описание: {task_info['description']}")
    print(f"Приоритет: {task_info['priority']}")
    print(f"Статус: {task_info['status']}")


def create_task(tasks: dict) -> None:
    """Создание новой задачи."""
    task_id = max(tasks.keys(), default=0) + 1
    title = input("Введите название задачи: ")
    description = input("Введите описание задачи: ")
    priority = input("Введите приоритет (1-Низкий, 2-Средний, 3-Высокий): ")

    while priority not in PRIORITIES:
        priority = input("Некорректный приоритет. Введите 1, 2 или 3: ")
    status = input("Введите статус (1-Новая, 2-В процессе, 3-Завершена): ")

    while status not in STATUSES:
        status = input("Некорректный статус. Введите 1, 2 или 3: ")
    tasks[task_id] = {
        "title": title,
        "description": description,
        "priority": PRIORITIES[priority],
        "status": STATUSES[status],
    }
    print(f"Задача {task_id} создана.")
    save_tasks(tasks)


def update_task(tasks: dict) -> None:
    """Обновление задачи."""
    try:
        task_id = int(input("Введите ID задачи для обновления: "))
    except ValueError:
        print("Некорректное значение ID задачи.")
        return

    if task_id not in tasks:
        print("Задача с таким ID не найдена.")
        return

    print("Что вы хотите обновить?")
    print("1 - Название\n2 - Описание\n3 - Приоритет\n4 - Статус")
    choice = input("Выберите действие (1-4): ")

    if choice == "1":
        title = input("Введите новое название: ").strip()
        tasks[task_id]["title"] = title
    elif choice == "2":
        description = input("Введите новое описание: ").strip()
        tasks[task_id]["description"] = description
    elif choice == "3":
        priority = input(
            "Введите новый приоритет (1-Низкий, 2-Средний, 3-Высокий): "
        ).strip()
        while priority not in PRIORITIES:
            priority = input(
                "Некорректный приоритет. Введите 1, 2 или 3: "
                ).strip()
        tasks[task_id]["priority"] = PRIORITIES[priority]
    elif choice == "4":
        status = input(
            "Введите новый статус (1-Новая, 2-В процессе, 3-Завершена): "
        ).strip()
        while status not in STATUSES:
            status = input("Некорректный статус. Введите 1, 2 или 3: ").strip()
        tasks[task_id]["status"] = STATUSES[status]
    else:
        print("Некорректный выбор.")

    print(f"Задача {task_id} обновлена.")
    save_tasks(tasks)


def delete_task(tasks: dict) -> None:
    """Удаление задачи."""
    try:
        task_id = int(input("Введите ID задачи для удаления: "))
    except ValueError:
        print("Некорректное значение ID должен быть целым числом.")
        return

    if task_id in tasks:
        del tasks[task_id]
        print(f"Задача {task_id} удалена.")
        save_tasks(tasks)
    else:
        print("Задача с таким ID не найдена.")


def view_tasks(tasks, sort_by=None, search_term=None):
    """Просмотр задач."""
    if sort_by == "status":
        sorted_tasks = sorted(tasks.items(), key=lambda x: x[1]["status"])
    elif sort_by == "priority":
        # Сортировка по приоритету: Низкий < Средний < Высокий
        sorted_tasks = sorted(
            tasks.items(),
            key=lambda x: list(PRIORITIES.values()).index(x[1]["priority"]),
        )
    else:
        sorted_tasks = tasks.items()

    if search_term:
        sorted_tasks = filter(
            lambda x: search_term.lower() in x[1]["title"].lower()
            or search_term.lower() in x[1]["description"].lower(),
            sorted_tasks,
        )

    sorted_tasks = list(sorted_tasks)

    if not sorted_tasks:
        print("Нет задач для отображения.")
        return

    for task_id, task_info in sorted_tasks:
        output_tasks(task_id, task_info)



def main_menu() -> None:
    """Главное меню."""
    tasks = load_tasks()

    while True:
        print("\n1 - Создать новую задачу")
        print("2 - Просмотреть задачи")
        print("3 - Обновить задачу")
        print("4 - Удалить задачу")
        print("0 - Выйти из программы")

        choice = input("Выберите действие (0-4): ")

        if choice == "1":
            create_task(tasks)
        elif choice == "2":
            while True:
                """Меню вложенного меню."""
                print("\n1 - Отобразить задачи в изначальном виде")
                print("2 - Отсортировать по статусу")
                print("3 - Отсортировать по приоритету")
                print("4 - Поиск по названию или описанию")
                print("0 - Выход в главное меню")
                sub_choice = input("Выберите действие (0-4): ")
                if sub_choice == "1":
                    view_tasks(tasks)
                elif sub_choice == "2":
                    view_tasks(tasks, sort_by="status")
                elif sub_choice == "3":
                    view_tasks(tasks, sort_by="priority")
                elif sub_choice == "4":
                    search_term = input("Введите строку для поиска: ")
                    view_tasks(tasks, search_term=search_term)
                elif sub_choice == "0":
                    break
        elif choice == "3":
            update_task(tasks)
        elif choice == "4":
            delete_task(tasks)
        elif choice == "0":
            print("Выход из программы.")
            break
        else:
            print("Некорректный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main_menu()