import os
import tempfile
import unittest

from psx.commands.todo import TodoStore, add_todo, complete_todo, list_todos, remove_todo


class TestTodoStore(unittest.TestCase):
    def test_add_and_list_todos(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            store = TodoStore(os.path.join(tmpdir, "todos.txt"))
            add_todo(store, "Write code")
            add_todo(store, "Ship feature")
            items = list_todos(store)
            self.assertEqual(len(items), 2)
            self.assertEqual(items[0]["task"], "Write code")

    def test_complete_and_remove_todos(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            store = TodoStore(os.path.join(tmpdir, "todos.txt"))
            add_todo(store, "Learn PSX")
            complete_todo(store, 1)
            remove_todo(store, 1)
            self.assertEqual(list_todos(store), [])


if __name__ == "__main__":
    unittest.main()
