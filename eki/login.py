import malupdate as mal
import getpass

from eki import fetch_login_cache, path_to_cache, clear

def login_auth(user, details):
    if 'access_token' in user.keys():
        print('Logged in as ' + details['username'] +'. Proceed? [Y/N]')
        n = input()
        n = n.lower()
        if n == 'yes' or n == 'y':
            pass
        else: 
            login()
    else:
        print('Wrong saved credentials. Log in again. \n')
        login()

def login(check_login: bool = False):
    # MyAnimeList login
    if check_login == True:
        details = fetch_login_cache()
        user = mal.User.login(details['username'], details['password'])
        login_auth(user, details)
    else:
        print('\nLogin to proceed.')
        username = input('Username: ')
        password = getpass.getpass('Password: ')
        with open(path_to_cache + 'login.txt', "w") as f:
            f.write("Username: " + username + '\n' + 'Password: ' + password)
        details = {
            'username': username, 'password': password
        }
        user = mal.User.login(username, password)
        login_auth(user, details)
    clear()
    return user