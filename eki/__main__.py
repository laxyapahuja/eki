import os
import re
import json
import sys
import requests

from pymediainfo import MediaInfo

from eki import check_login, anime_finder, path_to_cache, check_progress, progress_cache, clear, load_progress, fetch_login_cache
from eki.video_extensions import video_file_extensions
from eki.login import login, login_auth
from eki.tracker import track

user = {} # User Object
episode_info = [] # Episodes Information

def create_progress(path, check_progress: bool = False):
    if check_progress:
        pass
    else:
        with open(path + '\progress.txt', "wb") as f:
            f.write(json.dumps(progress_cache, indent=4).encode('utf-8'))

def findcommon(arr):
    if len(arr) <= 1:
        return None
    else:
        for bad in ['[', ']']:
            for i in range(len(arr)):
                arr[i] = arr[i].replace(bad, '')
        n = len(arr) 
        s = arr[0] 
        l = len(s)
        res = ''
        all_common = [] 
        for i in range(l) : 
            for j in range(i + 1, l + 1) : 
                stem = s[i:j] 
                k = 1
                for k in range(1, n):  
                    if stem not in arr[k]: 
                        break
                if (k + 1 == n and len(res) < len(stem)): 
                    res = stem
            if res in all_common:
                pass
            else:
                all_common.append(res)
        n=0
        for j in all_common:
            if j.endswith('0'):
                j = j.replace('0', '')
                all_common[n] = j
            n+=1
        return all_common

def episode_number_format(episode):
    m = str(episode).zfill(3)
    if m[0] == '0':
        m = str(episode).zfill(2)
    return m

def title_stripper(filename, common):
    filename = re.sub("[\(\[].*?[\)\]]", "", filename)
    for com in common:
        filename = filename.replace(com, '')
    return filename

def file_episode(check_progress):
    file_episodes = {}
    if check_progress:
        file_episodes = progress_cache['file_episodes']
    else:
        episodes = []
        for k in os.listdir():
            if k.endswith(video_file_extensions):
                episodes.append(k)
        common = findcommon(episodes)
        for i in range(1, int(progress_cache['anime_details']['episodes'])+1):
            for j in os.listdir():
                if common == None:
                    m = j
                else:
                    m = title_stripper(j, common)
                if str(episode_number_format(i)) in m or (common == None and j.endswith(video_file_extensions)):
                    file_episodes[str(i)] = j
                    break
    for ep in file_episodes:
        title = ''
        path = os.getcwd() + '\\' + file_episodes[ep]
        media_info = MediaInfo.parse(path)
        for track in media_info.tracks:
            if track.track_type == 'General':
                title = track.title
                if title == None:
                    title = file_episodes[ep]
        episode_dict = {
            'title': title,
            'path': path,
            'name': file_episodes[ep]
        }
        episode_info.append(episode_dict)
    progress_cache['file_episodes'] = file_episodes

def file_episodes_renamer(check_progress):
    API_URL = 'https://api.jikan.moe/v3/anime/'
    api_data = []
    file_episodes = progress_cache['file_episodes']
    response = requests.get(API_URL+str(progress_cache['anime_details']['mal_id'])+'/episodes').json()
    api_data = api_data + response['episodes']
    for i in range(2, response['episodes_last_page']+1):
        response = requests.get(API_URL+str(progress_cache['anime_details']['mal_id'])+'/episodes/'+str(i)).json()
        api_data = api_data + response['episodes']
    for key in file_episodes:
        for j in api_data:
            if key == str(j['episode_id']):
                new_filename = progress_cache['anime_details']['title'].replace(':', ' -').replace('?', '').replace('\\','').replace('/', '').replace('\"', '\'').replace('<','').replace('>','').replace('|','') + ' E' + episode_number_format(key) + ' - ' + j['title'].replace(':', ' -').replace('?', '').replace('\\','').replace('/', '').replace('\"', '\'').replace('<','').replace('>','').replace('|','') + '.' + file_episodes[key].split('.')[-1]
                if (file_episodes[key] == new_filename):
                    break
                else:
                    os.rename(str(os.getcwd() + '\\' + file_episodes[key]), str(os.getcwd() + '\\' + new_filename))
                    file_episodes[key] = new_filename
    progress_cache['file_episodes'] = file_episodes
    if check_progress:
        with open(os.getcwd() + '\progress.txt', "wb") as f:
            f.write(json.dumps(progress_cache, indent=4).encode('utf-8'))
    
def main():
    try:
        clear()
        print("Welcome to eki: Your local MyAnimeList tracker! \n")
        user = login(check_login())
        file_episode(check_progress())
        file_episodes_renamer(check_progress())
        create_progress(os.getcwd(), check_progress())
        track(episode_info, progress_cache, user)
    except KeyboardInterrupt:
        print('Omae Wa Mou Shindeiru.')
        sys.exit()

if __name__ == '__main__':
    main()