import datetime

from rich.console import Console
from rich.table import Table

import utils
from orm.admin_token_db import AdminTokenDB
from orm.todo_db import TodoDB
from orm.user_db import UserDB

from utils import UserUtils
from pages.userbase import BaseUserPage

from models.admin_token import  AdminToken


tododb = TodoDB()
userdb = UserDB()
admintokensdb = AdminTokenDB()

class BaseAdminPage(BaseUserPage):
    def add_admin_token(self):
        token_info = {}

        while True:
            email = input("Qaysi email egasi uchun admin token yaratmoqchisiz?(orqaga -> back):")
            if email.lower() == 'back':
                print("Yaxshi! Ortqaga qaytildi.")
                return
            if not utils.UserUtils.email_validator(email):
                print("Bu email yaroqsiz. Qayta urinib ko'ring.")
                continue
            token_info['email'] = email
            break

        token_info['created_by'] = self.user[0]

        token = AdminToken(**token_info)
        print(f"Siz yaratmoqchisiz:\n"
              f"{token.display()}")
        confirm = input("Hamma ma'lumotlar to'g'rimi?\n"
                        "Davom etamizmi? (yes or any):")
        if confirm.lower() != 'yes':
            print("Admin token yaratish bekor qilindi.")
            return None

        try:
            new_token = admintokensdb.add(token)
        except Exception as exc:
            print(f"Yaratish amalga oshmadi. Xato: {exc}")
        else:
            print(f"Admin token yaratildi. TOKEN: {new_token[2]}")
            return new_token



    def view_admin_tokens(self):
        tokens = admintokensdb.get_by_creator_id(self.user[0])
        if not tokens:
            print("Siz hali hech qanday admin token yaratmagansiz.")
            return

        console = Console()
        table = Table(title="Siz yaratgan admin tokenlar", show_header=True, header_style="bold cyan")
        table.add_column("T/r", justify="center")
        table.add_column("Email", style="bold")
        table.add_column("Token", justify="center")
        table.add_column("Status", justify="center")
        table.add_column("Expires At", justify="center")

        id_map = {}
        for idx, token in enumerate(tokens, 1):
            id_map[str(idx)] = token[0]
            status = "✅ Ishlatilgan" if token[4] else "❌ Ishlatilmagan"
            table.add_row(str(idx), token[1], token[2], status, UserUtils.time_formatter(str(token[5])))

        console.print(table)

        while True:
            select_index = input(
                "Ko‘rmoqchi bo‘lgan token tartib raqamini kiriting (orqaga qaytish uchun 'exit'): ").strip()
            if select_index.lower() == "exit":
                return None
            if select_index in id_map.keys():
                self.view_token_detail(id_map[select_index])
                break
            else:
                print("Noto‘g‘ri tanlov, qayta kiriting.")
    def view_token_detail(self, admin_token_id):
        token = admintokensdb.get_by_id(admin_token_id)
        if not token:
            print("Admin token topilmadi")
            return

        console = Console()
        console.print(f"\n[b]Email:[/b] {token[1]}")
        console.print(f"[b]Token:[/b] {token[2]}")
        console.print(f"[b]Yaratgan Admin ID:[/b] {token[3]}")
        console.print(f"[b]Holati:[/b] {'✅ Ishlatilgan' if token[4] else '❌ Ishlatilmagan'}")
        console.print(f"[b]Muddati tugash vaqti:[/b] {UserUtils.time_formatter(str(token[5]))}")
        console.print(f"[b]Yaratilgan vaqti:[/b] {UserUtils.time_formatter(str(token[6]))}")
        console.print(f"[b]Oxirgi yangilangan vaqti:[/b] {UserUtils.time_formatter(str(token[7]))}")

        print("🕒 1. Keyingi 24 soat uchun faollashtirish")
        print("🚫 2. Faolsizlantirish")
        print("🗑 3. O'chirish")
        print("🔙 4. Orqaga qaytish")

        while True:
            choise = input("Tanlovni kiriting:").strip()
            if choise == '1':
                self.update_admin_token(
                    admin_token_id,
                    {
                        'expires_at': datetime.datetime.now() + datetime.timedelta(hours=24)
                    }
                )
                break

            elif choise == '2':
                self.update_admin_token(admin_token_id, {'is_used': True})
                break
            elif choise == '3':
                self.delete_admin_token(admin_token_id)
                break
            elif choise == '4':
                print("Yaxshi! Orqaga qaytildi.")
                break
            else:
                print("Noto'g'ri tanlov, qayta kiriting.")

    def delete_admin_token(self, token_id):
        confirm = str(input("Rostdan ham tokenni o'chirishni xoxlaysizmi? (yes or any):"))
        if confirm.lower() == 'yes':
            admintokensdb.delete_by_id(token_id)
            print("❌ Token o‘chirildi.")
            return True
        else:
            print("O'chirish bekor qilindi.")
            return False

    def update_admin_token(self, token_id, new_data):
        try:
            admintokensdb.update_admin_token(token_id, new_data)
        except Exception as err:
            print(f"❌O'zgarish amalga oshmadi. Xato: {err}")
            return False
        else:
            print("✅ O'zgarishlar amalga oshdi.")
            return True


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
        users = userdb.get_all(self.user[0])
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

        while True:
            select_index = input("Ko‘rmoqchi bo‘lgan userning tartib raqamini kiriting (orqaga qaytish uchun 'exit'): ").strip()
            if select_index.lower() == "exit":
                return None
            if select_index in id_map.keys():
                self.user_check(id_map[select_index])
                break
            else:
                print("Noto‘g‘ri tanlov, qayta kiriting.")


    def user_check(self, user_id):
        user = userdb.get_by_id(user_id)
        if not user:
            print("Foydalanuvchi topilmadi.")
            return None

        console = Console()
        console.print(f"\n[b]Username:[/b] {user[1]}")
        console.print(f"[b]Email:[/b] {user[2]}")
        console.print(f"[b]Role:[/b] {user[3]}")
        console.print(f"[b]Yaratilgan vaqti:[/b] {UserUtils.time_formatter(str(user[5]))}")
        console.print(f"[b]Oxirgi yangilangan vaqti:[/b] {UserUtils.time_formatter(str(user[6]))}\n")

        print("1. ✏️ Userga admin rolini berish")
        print("2. 🔑 Userning Todolarini ko'rish")
        print("3. ❌ Userni o‘chirish")
        print("4. 🔙 Orqaga qaytish")

        while True:
            choice = input("Tanlovni kiriting: ").strip()
            if choice == '1':
                self.make_admin(user_id)
                break
            elif choice == '2':
                self.view_todos(user_id)
                break
            elif choice == '3':
                res = self.delete_user(user_id)
                if res:
                    return 'deleted'
                else:
                    return 'cancelled'
            elif choice == '4':
                return None
            else:
                print("Noto'g'ri tanlov, qayta kiriting.")
    def make_admin(self, user_id):
        user = userdb.get_by_id(user_id)
        if not user:
            print("Foydalanuvchi topilmadi.")
            return None
        if user[3] == 'admin':
            print("Bu profil egasi allaqachon admin.")
            return None

        confirm = input(f"Rostdan ham {user[1]} profil egasini admin qilmoqchimisiz? (yes or any): ")
        if confirm.lower() == 'yes':
            try:
                userdb.update(user_id, {'role': 'admin'})
            except Exception as err:
                print(f"Admin qilishda xatolik: {err}")
            else:
                print(f"Yaxshi! {user[1]} endi admin.")
                self.user_check(user_id)
        else:
            print("Admin qilish bekor qilindi.")











