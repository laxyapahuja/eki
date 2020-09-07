import os
import requests
import json

path_to_cache = os.getenv('LOCALAPPDATA') + '\\eki\\' #path to login cache
jikan_anime_search = "https://api.jikan.moe/v3/search/anime?q=" # Jikan search API endpoint
jikan_anime = 'https://api.jikan.moe/v3/anime/' # Jikan Anime API endpoint

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def check_progress():
    # Checks if progress cache is present
    if os.path.exists(os.getcwd() + '\progress.txt'):
        return True
    else:
        return False

def load_progress():
    if check_progress() == True:
        f = open(os.getcwd() + '\progress.txt', encoding='utf-8', errors='ignore')
        local_progress_cache = json.loads(str(f.read().replace("\'", "\"")))
        f.close()
    else:
        return {}
    return local_progress_cache

progress_cache = load_progress()

def check_login():
    # Checks if login cache is present
    if os.path.exists(path_to_cache + 'login.txt'):
        return True
    else:
        if os.path.exists(path_to_cache) == False:
            os.mkdir(path_to_cache)
        return False

def fetch_login_cache():
    if check_login() == True:
        f = open(path_to_cache + 'login.txt')
        login_info_cache = f.read()
        username = login_info_cache.split('\n')[0].split(':')[1].strip()
        password = login_info_cache.split('\n')[1].split(':')[1].strip()
        f.close()
        details = {
            'username': username,
            'password': password
        }
        return details

def anime_finder(path, correct: bool = True, anime: str = None):
    # Finds the anime and prompts the user to confirm it 
    anime_details = {}
    if check_progress() == True:
        anime_details = progress_cache['anime_details']
        print('Title: ' + anime_details['title'] + '\n' + 'MAL URL: ' + anime_details['url'] + '\n' + 'loaded from progress.txt. If you think it\'s wrong, delete progress.txt and run eki again.')
    else:
        if anime != None:
            anime_title = anime
        else:
            anime_title = path.split('\\')[-1]
        response = requests.get(jikan_anime_search + anime_title).json()["results"]
        if correct:
            clear()
            print('Title: ' + response[0]['title'] + '\n' + 'MAL URL: ' + response[0]['url'])
            n = input('Is this the correct title? [Y/N] \n')
            if n == 'yes' or n == 'y':
                anime_details = {
                'title': response[0]['title'],
                'mal_id': response[0]['mal_id'],
                'url': response[0]['url'],
                'episodes': response[0]['episodes']
                }
            else:
                anime_details = anime_finder(os.getcwd(), False)
        else:
            try:
                clear()
                print('Choose the correct title: [1-5/n]')
                for i in range(5):
                    print(str(i+1)+'. ' + response[i]['title'] + '\n' + response[i]['url'] + '\n')
                choice = int(input("Correct title: "))
                anime_details = {
                    'title': response[choice - 1]['title'],
                    'mal_id': response[choice - 1]['mal_id'],
                    'url': response[choice -1]['url'],
                    'episodes': response[choice - 1]['episodes']
                }
                return anime_details
            except:
                clear()
                inp = input('Manual Search: ')
                anime_details = anime_finder(os.getcwd(), False, inp)
    duration = requests.get(jikan_anime + str(anime_details['mal_id'])).json()["duration"]
    anime_details['duration'] = duration
    progress_cache['anime_details'] = anime_details
    return anime_details

progress_cache['anime_details'] = anime_finder(os.getcwd())