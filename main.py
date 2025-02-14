""""Bu yerga hamma mehmanizmlarni yigib turadigan asosiy kodlar yoziladi"""
from pages.home import HomePage
from pages.userbase import BaseUserPage
from pages.adminbase import BaseAdminPage

def admin_panel(basepage: BaseAdminPage):
    while True:
        text = ""
        text += "Siz admin paneldasiz!\n"
        text += "1. Barcha userlarni ko'rish\n"
        text += "2. Barcha Todolarni ko'rish\n"
        text += "3. Admin paneldan chiqish"
        print(text)

        choise = input("Tanlovingiz: ").strip()

        if choise == '1':
            basepage.view_all_users()
        elif choise == '2':
            basepage.view_all_todos()
        elif choise == '3':
            print("Admin paneldan chiqdingiz.")
            break
        else:
            print("Noto'g'ri tanlov! Qaytadan urinib ko'ring.")


def profil(basepage: BaseAdminPage | BaseUserPage):
    while True:
        text = ""
        text += "Siz profildasiz!\n"
        text += "1. Profilni o'chirish\n"
        text += "2. Profilni yangilash\n"
        text += "3. Profil paneldan chiqish"
        print(text)

        choise = input("Tanlovingiz: ").strip()

        if choise == '1':
            basepage.delete_user(basepage.user[0])
            return 'deleted'
        elif choise == '2':
            basepage.update_user(basepage.user[0], basepage.user)
        elif choise == '3':
            print("Profil paneldan chiqdingiz.")
            break
        else:
            print("Noto'g'ri tanlov! Qaytadan urinib ko'ring.")




def main():
    while True:
        choice = input("\n1. Register\n"
                       "2. Login\n"
                       "3. Dasturni tugatish\n"
                       "Tanlov: ").strip()

        if choice == '1':
            HomePage.register()

        elif choice == '2':
            user = HomePage.login()
            if user:
                if user[3] != "admin":
                    base_page = BaseUserPage(user)
                else:
                    base_page = BaseAdminPage(user)
                while True:
                    text = "\nBase menyu:\n"
                    text += "1. Todo qo'shish\n"
                    text += "2. Todolarimni ko'rish\n"
                    text += "3. Profilga kirish\n"
                    text += "4. Logout (Home ga qaytish)"
                    text += "\nadm. Admin panelga kirish" if base_page.user[3] == 'admin' else ""
                    print(text)

                    base_choice = input("Tanlovingiz: ").strip()

                    if base_choice == '1':
                        base_page.add_todo()
                    elif base_choice == '2':
                        base_page.view_todos(base_page.user[0])
                    elif base_choice == '3':
                        if base_page.view_user_detail() == 'deleted':
                            break
                        continue
                    elif base_choice == '4':
                        print("Bosh sahifaga qaytildi.")
                        break
                    elif base_choice == 'adm' and base_page.user[3] == 'admin':
                        admin_panel(base_page)
                    else:
                        print("Noto'g'ri tanlov! Qaytadan urinib ko'ring.")
            else:
                print("Login muvaffaqiyatsiz yakunlandi.")

        elif choice == '3':
            print("Dastur tugatildi.")
            break

        else:
            print("Noto'g'ri tanlov! Qaytadan urinib ko'ring.")

if __name__ == "__main__":
    main()