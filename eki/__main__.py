import os
import malupdate as mal
import getpass

from eki import check_login, anime_finder, path_to_cache, check_progress

user = {}
anime_details = {}

def login(check_login: bool = False):
    if check_login == True:
        f = open(path_to_cache + 'login.txt')
        login_info_cache = f.read()
        username = login_info_cache.split('\n')[0].split(':')[1].strip()
        password = login_info_cache.split('\n')[1].split(':')[1].strip()
        user = mal.User.login(username, password)
        if 'access_token' in user.keys():
            print('Logged in as ' + username +'. Proceed? [Y/N]')
            n = input().lower()
            if n == 'yes' or n == 'y':
                pass
            else: 
                login(False)
        else:
            print('Wrong saved credentials. Log in again. \n')
            login(False)
    else:
        print('\nLogin to proceed.')
        username = input('Username: ')
        password = getpass.getpass('Password: ')
        with open(path_to_cache + 'login.txt', "w") as f:
            f.write("Username: " + username + '\n' + 'Password: ' + password)
        user = mal.User.login(username, password)
        print(user)

def create_progress(path, anime_details, check_progress: bool = False):
    if check_progress == True:
        pass
    else:
        with open(path + '\progress.txt', "w") as f:
            f.write(str(anime_details))

def main():
    print("Welcome to Local MAL Tracker! \n")
    login(check_login())
    anime_details = anime_finder(os.getcwd())
    create_progress(os.getcwd(), anime_details, check_progress())

if __name__ == '__main__':
    main()