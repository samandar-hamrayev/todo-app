from datetime import datetime, timedelta

from models.user_model import User
from models.todo_model import Todo


from orm.todo_db import TodoDB
from orm.user_db import UserDB



userdb = UserDB()
tododb = TodoDB()


user1 = User('samandar', 'samandar@gmail.com', 'admin', 'password')
user2 = User('mamur', 'mamur@gmail.com', 'user', 'password')

# userdb.add(user1)
# userdb.add(user2)

todo_samandar1 = Todo(1,
                     'kursga borish',
                     'kursga 1 dan keyin borish kerak',
                     'low',
                     datetime.now() + timedelta(days=1, hours=0))

todo_samandar2 = Todo(1,
                     'kursga borish',
                     'kursga 1 dan keyin borish kerak',
                     'high',
                     datetime.now() + timedelta(days=1, hours=0))

todo_mamur1 = Todo(2,
                      'oqishga borish',
                     'oqishga borish ',
                     'medium',
                     datetime.now() + timedelta(days=3, hours=0))

tododb.add(todo_samandar1)
tododb.add(todo_samandar2)
tododb.add(todo_mamur1)


all_users = userdb.get_all()
for user in all_users:
    id, username, email, role,  created_at, updated_at = user
    ctime = str(created_at)
    form_time = datetime.strptime(ctime, "%Y-%m-%d %H:%M:%S.%f").strftime("%Y-%m-%d %H-%M-%S")
    print(f"id:{id}\n"
          f"username:{username}\n"
          f"email:{email}\n"
          f"role:{role}\n"
          f"creaeted at: {form_time}")