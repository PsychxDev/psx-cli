import os
import sys

from psx.utils.display import header, sep


class TodoStore:
    def __init__(self, path: str = None):
        self.path = path or os.path.join(os.path.expanduser("~"), ".psx_todos.txt")

    def _load(self) -> list[dict]:
        if not os.path.exists(self.path):
            return []

        items = []
        with open(self.path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                parts = line.split("|", 1)
                if len(parts) == 2:
                    done, task = parts
                    items.append({"id": len(items) + 1, "task": task.strip(), "done": done.strip() == "1"})
        return items

    def _save(self, items: list[dict]) -> None:
        with open(self.path, "w", encoding="utf-8") as file:
            for item in items:
                file.write(f"{'1' if item['done'] else '0'}|{item['task']}\n")

    def add(self, task: str) -> dict:
        items = self._load()
        todo = {"id": len(items) + 1, "task": task.strip(), "done": False}
        items.append(todo)
        self._save(items)
        return todo

    def list(self) -> list[dict]:
        return self._load()

    def complete(self, item_id: int) -> dict | None:
        items = self._load()
        for item in items:
            if item["id"] == item_id:
                item["done"] = True
                self._save(items)
                return item
        return None

    def remove(self, item_id: int) -> bool:
        items = self._load()
        filtered = [item for item in items if item["id"] != item_id]
        if len(filtered) == len(items):
            return False
        for index, item in enumerate(filtered, start=1):
            item["id"] = index
        self._save(filtered)
        return True


def add_todo(store: TodoStore, task: str) -> dict:
    return store.add(task)


def list_todos(store: TodoStore) -> list[dict]:
    return store.list()


def complete_todo(store: TodoStore, item_id: int) -> dict | None:
    return store.complete(item_id)


def remove_todo(store: TodoStore, item_id: int) -> bool:
    return store.remove(item_id)


def print_todos(items: list[dict]) -> None:
    if not items:
        print("No tasks found.")
        return

    for item in items:
        status = "[x]" if item["done"] else "[ ]"
        print(f"{status} {item['id']}. {item['task']}")


def run(action: str = None, value: str = None) -> None:
    store = TodoStore()
    length = header("Todo")

    action = (action or "list").lower()

    if action == "add":
        if not value:
            print("Usage: psx todo add <task>")
            sep(length)
            return
        item = add_todo(store, value)
        print(f"Added: {item['task']}")
        sep(length)
        return

    if action == "done":
        if not value or not value.isdigit():
            print("Usage: psx todo done <id>")
            sep(length)
            return
        item = complete_todo(store, int(value))
        if item:
            print(f"Completed: {item['task']}")
        else:
            print("Task not found.")
        sep(length)
        return

    if action == "remove":
        if not value or not value.isdigit():
            print("Usage: psx todo remove <id>")
            sep(length)
            return
        removed = remove_todo(store, int(value))
        if removed:
            print(f"Removed task #{value}")
        else:
            print("Task not found.")
        sep(length)
        return

    if action == "list":
        print_todos(list_todos(store))
        sep(length)
        return

    print("Usage: psx todo [list|add|done|remove]")
    sep(length)
