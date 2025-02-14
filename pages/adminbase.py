from rich.console import Console
from rich.table import Table

from pages.userbase import BaseUserPage
from orm.todo_db import TodoDB
from orm.user_db import UserDB
from utils import UserUtils


tododb = TodoDB()
userdb = UserDB()

class BaseAdminPage(BaseUserPage):
    def view_all_todos(self):
        todos = tododb.get_all()
        if not todos:
            print("Foydalanuvchilar hali todo yaratmagan.")
            return

        console = Console()
        table = Table(title="Tizimdagi hamma todolar", show_header=True, header_style="bold cyan")
        table.add_column("T/r", justify="center")
        table.add_column("Title", style="bold")
        table.add_column("Status", justify="center")
        table.add_column("Due Date", justify="center")

        id_map = {}
        for idx, todo in enumerate(todos, 1):
            id_map[str(idx)] = todo[0]
            status = "✅ Bajarildi" if todo[6] else "❌ Bajarilmagan"
            table.add_row(str(idx), todo[2], status, UserUtils.time_formatter(str(todo[5])))
        console.print(table)

        while True:
            select_index = input("Ko‘rmoqchi bo‘lgan todo tartib raqamini kiriting (orqaga qaytish uchun 'exit'): ").strip()
            if select_index.lower() == "exit":
                return None
            if select_index in id_map.keys():
                self.view_todo_detail(id_map[select_index])
                break
            else:
                print("Noto‘g‘ri tanlov, qayta kiriting.")

    def view_all_users(self):
        users = userdb.get_all()
        if not users:
            print("Hali userlar mavjud emas.")
            return

        console = Console()
        table = Table(title="Foydalanuvchilar ro'yxati", show_header=True, header_style="bold cyan")

        table.add_column("T/r", justify="center")
        table.add_column("Username", style="bold")
        table.add_column("Email", style="bold magenta")
        table.add_column("Role", justify="center")
        table.add_column("Created At", justify="center")
        table.add_column("Updated At", justify="center")
        table.add_column("Todo Count", justify="center", style="bold yellow")

        id_map = {}
        for idx, user in enumerate(users, 1):
            id_map[str(idx)] = user[0]
            table.add_row(str(idx), user[1], user[2], user[3], UserUtils.time_formatter(str(user[4])), UserUtils.time_formatter(str(user[5])), str(user[6]))

        console.print(table)







