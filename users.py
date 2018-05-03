users = []
def add_user(name, email, username, password):
    user = {}
    user['name'] = name
    user['email'] = email
    user['username'] = username
    user['password'] = password
    users.append(user)

def get_user_password(username):
    flag = False
    for every_user in users:
        values = every_user.values()
        if username in values:
            flag = True
            password = every_user['password']
            break

    if flag:
        response = {'found' : True,
                    'password' : password
        }
    else:
        response = {'found' : False,
                    'password' : ''
        }
    return response
