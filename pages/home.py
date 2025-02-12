from utils import UserUtils as uu
from orm.user_db import UserDB
from models.user_model import User

userdb = UserDB()

class HomePage:
    @staticmethod
    def register() -> None | tuple:
        user_info = {}

        def get_input(prompt: str, validator=None, db_check=None, error_msg="Yaroqsiz qiymat!", home_exit=True):
            while True:
                value = str(input(prompt)).strip()
                if home_exit and value.lower() == "home":
                    print("Bosh sahifaga qaytildi.")
                    return "home"
                if validator and not validator(value):
                    print(error_msg)
                    continue
                if db_check and db_check(value) is not None:
                    print("Bu ma’lumot bilan foydalanuvchi mavjud, boshqa kiriting.")
                    continue
                return value

        username = get_input("Username kiriting:", uu.username_validator, userdb.get_by_username, "Yaroqsiz username!")
        if username == "home":
            return None
        user_info["username"] = username

        email = get_input("Email kiriting:", uu.email_validator, userdb.get_by_email, "Yaroqsiz email!")
        if email == "home":
            return None
        user_info["email"] = email

        password = get_input("Parol kiriting (Katta, kichik harf, raqam va punktuatsiya kerak):", uu.password_validator, None, "Parol juda oddiy!")
        if password == "home":
            return None
        user_info["password"] = password

        role = get_input("Qanday rol (user/admin):", lambda r: r.lower() in ["user", "admin"], None, "Faqat 'user' yoki 'admin' tanlang!")
        if role == "home":
            return None
        user_info["role"] = role.lower()

        user = User(**user_info)
        print(f"Sizning ma’lumotlaringiz:\n{user.display()}")

        confirmation = get_input("Davom etamizmi? (yes/no):", lambda c: c.lower() in ["yes", "no"], None, "Faqat 'yes' yoki 'no' tanlang!")
        if confirmation == "home" or confirmation == "no":
            print("Ro‘yxatdan o‘tish bekor qilindi.")
            return None

        try:
            new_user = userdb.add(user)
        except Exception:
            print("Nimadir xato bo‘ldi, qayta urinib ko‘ring.")
            return None
        else:
            print(f"Siz ro‘yxatdan o‘tdingiz! ID: {new_user[0]}")
            return new_user

    @staticmethod
    def login() -> None | tuple:
        """Foydalanuvchini tizimga kiritish"""
        def get_input(prompt: str, validator=None, home_exit=True):
            """Umumiy input olish funksiyasi, home qaytish qo‘shilgan"""
            while True:
                value = str(input(prompt)).strip()
                if home_exit and value.lower() == "home":
                    print("Bosh sahifaga qaytildi.")
                    return "home"
                if validator and not validator(value):
                    print("Yaroqsiz ma’lumot! Qayta urining.")
                    continue
                return value

        login_value = get_input("ID, email yoki username'ingizni kiriting:", lambda x: x.isdigit() or uu.username_validator(x) or uu.email_validator(x))
        if login_value == "home":
            return None

        password = get_input("Parolingizni kiriting:", lambda x: len(x) > 0)
        if password == "home":
            return None

        if login_value.isdigit():
            user = userdb.get_by_id(int(login_value))
        elif uu.username_validator(login_value):
            user = userdb.get_by_username(login_value)
        elif uu.email_validator(login_value):
            user = userdb.get_by_email(login_value)
        else:
            print("Login yoki parol xato.")
            return None

        if user is not None and uu.verify_password(password, user[4]):
            print("Siz tizimga kirdingiz!")
            return user
        else:
            print("Login yoki parol xato.")
            return None


# print(HomePage.register())

from rich.console import Console
from rich.table import Table

console = Console()
table = Table(title="Todo List")
table.add_column("ID", style="cyan")
table.add_column("Vazifa", style="magenta")
table.add_column("Holat", style="green")

table.add_row("1", "Python o‘rganish", "Bajarilmagan")
table.add_row("2", "Leetcode 3 ta masala yechish", "Bajarilgan")
console.print(table)