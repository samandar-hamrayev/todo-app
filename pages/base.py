from rich.console import Console
from rich.table import Table


import datetime
from models.todo_model import Todo
from utils import UserUtils

from laboratoroya import username
from orm.todo_db import TodoDB



tododb = TodoDB()

class BasePage:
    def __init__(self, user):
        self.user = user

class BaseUserPage(BasePage):
    def view_todos(self):
        todos = tododb.get_by_user_id(self.user[0])
        if not todos:
            print("Sizda hali todo mavjud emas.")
            return
        console = Console()
        table = Table(title="Sizning Todolaringiz", show_header=True, header_style="bold cyan")
        table.add_column("T/r", justify="center")
        table.add_column("Title", style="bold")
        table.add_column("Status", justify="center")
        table.add_column("Due Date", justify="center")

        id_map = {}
        for idx, todo in enumerate(todos, 1):
            id_map[idx] = todo[0]
            status = "✅ Bajarildi" if todo[6] else "❌ Bajarilmagan"
            table.add_row(str(idx), todo[2], status, todo[5])
        console.print(table)

        while True:
            """todoni batafsil korish uchun index kiritish"""
            pass

    def view_todo_detail(self, todo_id):
        todo = tododb.get_by_id(todo_id)
        if not todo:
            print("Todo topilmadi.")
            return None

        console = Console()
        console.print(f"\n[b]Title:[/b] {todo[2]}")
        console.print(f"[b]Description:[/b] {todo[3]}")
        console.print(f"[b]Priority:[/b] {todo[4]}")
        console.print(f"[b]Status:[/b] {'✅ Bajarildi' if todo[6] else '❌ Bajarilmagan'}")
        console.print(f"[b]Oxirgi muddat:[/b] {todo[5]}\n")
        console.print(f"[b]Yaratilgan muddat:[/b] {todo[7]}\n")
        console.print(f"[b]Oxirgi yangilangan muddat:[/b] {todo[8]}\n")

        print("1. ✅ Bajarilgan deb belgilash")
        print("2. ✏️ Yangilash")
        print("3. ❌ O‘chirish")
        print("4. 🔙 Orqaga qaytish")

        while True:
            choise = str(input("Tanlovni kiriting:")).strip()
            if choise == '1':
                self.mark_todo_done(todo_id)
                break
            elif choise == '2':
                self.update_todo(todo_id, todo)
                break
            elif choise == '3':
                self.delete_todo(todo_id)
            elif choise == '4':
                return None
            else:
                print("Noto'g'ri tanlov, qayta kiriting.")

    def mark_todo_done(self, todo_id):
        tododb.update(todo_id, {'status', True})
        print("✅ Todo bajarildi deb belgilandi.")

    def delete_todo(self, todo_id):
        confirm = str(input("Rostdan ham todoni o'chirishni xoxlaysizmi? (yes or any):"))
        if confirm.lower() == 'yes':
            tododb.delete(todo_id)
            print("❌ Todo o‘chirildi.")
        else:
            print("O'chirish bekor qilindi.")


    def update_todo(self, todo_id, old_todo):
        todo_info = {}

        def get_input(prompt, validator=None, error_msg="Noto‘g‘ri qiymat!", old_value=None):
            while True:
                value = input(prompt).strip()
                if not value:
                    return old_value
                if validator and not validator(value):
                    print(error_msg)
                    continue

                return value
        title = get_input("Sarlavha (hozirgi: {}): ".format(old_todo[2]),
                          lambda txt: not txt.isdigit(),
                          "Sarlavha raqamlardan iborat bo‘lishi mumkin emas!",
                          old_todo[2])

        description = get_input("Tavsif (hozirgi: {}): ".format(old_todo[3]),
                                lambda txt: len(txt) > 0,
                                "Tavsif bo‘sh bo‘lmasligi kerak.",
                                old_todo[3])

        priority = get_input("Priority (low, medium yoki high, hozirgi: {}): ".format(old_todo[4]),
                             lambda pr: pr.lower() in ['low', 'medium', 'high'],
                             "Faqat low, medium yoki high.",
                             old_todo[4])

        while True:
            days = input("Oxirgi muddat - necha kun? (hozirgi: {} kun): ".format(old_todo[5].days)).strip()
            hours = input(
                "Oxirgi muddat - necha soat? (hozirgi: {} soat): ".format(old_todo[5].seconds // 3600)).strip()

            if not days:
                days = old_todo[5].days
            if not hours:
                hours = old_todo[5].seconds // 3600

            try:
                days = int(days)
                hours = int(hours)
                due_date = datetime.datetime.now() + datetime.timedelta(days=days, hours=hours)
                break
            except ValueError:
                print("❌ Kun va soat faqat raqamlardan iborat bo‘lishi kerak!")

        todo_info = {
            "title": title,
            "description": description,
            "priority": priority.lower(),
            "due_date": due_date
        }

        try:
            tododb.update(todo_id, todo_info)
            print("✅ Todo muvaffaqiyatli yangilandi!")
        except Exception as err:
            print(f"❌ Xatolik yuz berdi: {err}")

    def add_todo(self):
        todo_info = {}

        def get_input(prompt: str, validator=None, db_check=None, error_msg="Yaroqsiz qiymat!", base_exit=True):
            while True:
                value = input(prompt).strip()
                if base_exit and value.lower() == 'base':
                    print("Asosiy ishlash sahifasiga qaytildi.")
                    return "base"
                if validator and not validator(value):
                    print(error_msg)
                    continue
                if db_check and db_check(value):
                    print("Bu ma'lumot bilan sizda todo mavjud, boshqa kiriting.")
                    continue
                return value

        title = get_input("Title kiriting:",
                          lambda txt: not txt.isdigit(),
                          tododb.get_by_title_from_user,
                          "Title faqat raqam bo'lmasligi kerak")
        if title == "base":
            return None
        todo_info['title'] = title

        description = get_input("Description kiriting (bo'sh bo'lmasin):",
                                lambda txt: len(txt) != 0,
                                None,
                                "Description bo'sh bo'lmasligi kerak.")
        if description == "base":
            return None
        todo_info['description'] = description

        priority = get_input("Priority kiriting (low, medium yoki high):",
                             lambda pr: pr.lower() in ['low', 'medium', 'high'],
                             None,
                             "Faqat low, medium yoki high dan birini tanlang.")
        if priority == "base":
            return None
        todo_info['priority'] = priority.lower()

        delta_day = get_input("Todoning yakuniy muddati necha kundan keyin (1 dan 10 gacha):",
                              lambda day: day.isdigit() and 1 <= int(day) <= 10,
                              None,
                              "Kun 1 dan 10 gacha bo'lishi kerak.")
        if delta_day == "base":
            return None
        delta_day = int(delta_day)

        delta_hour = get_input(f"Todo yakuniy muddati {delta_day} kun va qancha soat keyin (0 dan 24 gacha):",
                               lambda hour: hour.isdigit() and 0 <= int(hour) <= 24,
                               None,
                               "Soat 0 dan 24 gacha bo'lishi kerak.")
        if delta_hour == "base":
            return None
        delta_hour = int(delta_hour)

        todo_info['due_date'] = datetime.datetime.now() + datetime.timedelta(days=delta_day, hours=delta_hour)
        todo_info['user_id'] = self.user[0]

        todo = Todo(**todo_info)
        try:
            new_todo = tododb.add(todo)
        except Exception as err:
            print(f"❌ Todo yaratilmadi, xato: {err}")
        else:
            print(f"✅ Todo yaratildi! ID: {new_todo[0]}")



class BaseAdminPage(BasePage):
    pass
