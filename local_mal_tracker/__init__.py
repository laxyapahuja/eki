import os, requests, json

path_to_cache = os.getenv('LOCALAPPDATA') + '\\LocalMALTracker\\'
jikan_anime_search = "https://api.jikan.moe/v3/search/anime?q="

def check_login():
    if os.path.exists(path_to_cache + 'login.txt'):
        return True
    else:
        if os.path.exists(path_to_cache) == False:
            os.mkdir(path_to_cache)
        return False

def check_progress():
    if os.path.exists(os.getcwd() + '\progress.txt'):
        return True
    else:
        return False

def anime_finder(path, correct: bool = True):
    anime_details = {}
    if check_progress() == True:
        f = open(os.getcwd() + '\progress.txt')
        anime_details = json.loads(f.read().replace("\'", "\""))
        f.close()
        print('\nTitle: ' + anime_details['title'] + '\n' + 'MAL URL: ' + anime_details['url'])
        n = input('Is this the correct title? [Y/N] \n')
        if n == 'yes' or n == 'y':
            pass
        else:
            os.remove(os.getcwd() + '\progress.txt')
            anime_details = anime_finder(os.getcwd(), True)
    else:
        anime_title = path.split('\\')[-1]
        response = requests.get(jikan_anime_search + anime_title).json()["results"]
        if correct:
            print('\nTitle: ' + response[0]['title'] + '\n' + 'MAL URL: ' + response[0]['url'])
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
            print('\nChoose the correct title: [1-5]')
            for i in range(5):
                print(str(i+1)+'. ' + response[i]['title'] + '\n' + response[i]['url'] + '\n')
            choice = int(input("Correct title: "))
            anime_details = {
                'title': response[choice - 1]['title'],
                'mal_id': response[choice - 1]['mal_id'],
                'url': response[choice -1]['url'],
                'episodes': response[0]['episodes']
            }
            return anime_details
    return anime_details
