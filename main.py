""""Bu yerga hamma mehmanizmlarni yigib turadigan asosiy kodlar yoziladi"""
from pages.home import HomePage
from pages.userbase import BaseUserPage

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
                base_page = BaseUserPage(user)
                while True:
                    print("\nBase menyu:")
                    print("1. Todo qo'shish")
                    print("2. Todosni ko'rish")
                    print("3. Logout (Home ga qaytish)")

                    base_choice = input("Tanlovingiz: ").strip()

                    if base_choice == '1':
                        base_page.add_todo()
                    elif base_choice == '2':
                        base_page.view_todos()
                    elif base_choice == '3':
                        print("Bosh sahifaga qaytildi.")
                        break
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