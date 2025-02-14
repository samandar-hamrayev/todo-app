from pages.home import HomePage
from pages.userbase import BaseUserPage
from pages.adminbase import BaseAdminPage


def show_menu(options):
    print("\n" + "\n".join(f"{i}. {opt}" for i, opt in enumerate(options, 1)))

def admin_panel(basepage: BaseAdminPage):
    while True:
        show_menu(["Barcha userlarni ko'rish", "Barcha Todolarni ko'rish", "Admin paneldan chiqish"])
        choice = input("Tanlovingiz: ").strip()
        if choice == '1':
            basepage.view_all_users()
        elif choice == '2':
            basepage.view_all_todos()
        elif choice == '3':
            print("Admin paneldan chiqdingiz.")
            break
        else:
            print("Noto'g'ri tanlov! Qaytadan urinib ko'ring.")


def user_menu(base_page):
    while True:
        options = ["Todo qo'shish", "Todolarimni ko'rish", "Profilga kirish", "Logout"]
        if base_page.user[3] == 'admin':
            options.append("Admin panelga kirish")
        show_menu(options)

        choice = input("Tanlovingiz: ").strip()
        if choice == '1':
            base_page.add_todo()
        elif choice == '2':
            base_page.view_todos(base_page.user[0])
        elif choice == '3':
            if base_page.view_user_detail() == 'deleted':
                break
        elif choice == '4':
            print("Bosh sahifaga qaytildi.")
            break
        elif choice == '5' and base_page.user[3] == 'admin':
            admin_panel(base_page)
        else:
            print("Noto'g'ri tanlov! Qaytadan urinib ko'ring.")


def main():
    while True:
        show_menu(["Register", "Login", "Dasturni tugatish"])
        choice = input("Tanlov: ").strip()

        if choice == '1':
            HomePage.register()
        elif choice == '2':
            user = HomePage.login()
            if user:
                base_page = BaseAdminPage(user) if user[3] == "admin" else BaseUserPage(user)
                user_menu(base_page)
            else:
                print("Login muvaffaqiyatsiz yakunlandi.")
        elif choice == '3':
            print("Dastur tugatildi.")
            break
        else:
            print("Noto'g'ri tanlov! Qaytadan urinib ko'ring.")

if __name__ == "__main__":
    main()
