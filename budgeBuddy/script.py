from app import User,db,app

user = User.query.all()
if user:
    for i in user:
        print(f"Name: {i.Username}, email: {i.email}, Password: {i.password}")
else:
    print("The DB is empty")
