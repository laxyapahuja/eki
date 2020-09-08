import win32gui
import time
import sys

from threading import Timer

from eki import clear
from eki.mal import update_ep, update_status

def get_episode(episode_info, progress_cache, user):
    current_episode = []
    def winEnumHandler(hwnd, ctx):
        if win32gui.IsWindowVisible(hwnd) and 'VLC' in win32gui.GetWindowText(hwnd):
            for episode in episode_info:
                if episode['title'] in win32gui.GetWindowText(hwnd):
                    for ep in progress_cache['file_episodes']:
                        if episode['name'] == progress_cache['file_episodes'][ep] and episode['title'] in win32gui.GetWindowText(hwnd):
                            current_episode.append(int(ep))
    win32gui.EnumWindows(winEnumHandler, None)
    return current_episode

def duration_parser(progress_cache):
    time_in_secs = 0
    duration = progress_cache['anime_details']['duration']
    duration = duration.replace('.', '').replace(' ', '')
    if 'hr' in duration and 'min' in duration:
        duration = duration.split('hr')
        hours = int(duration[0])
        time_in_secs = time_in_secs + hours*60*60
        duration[1] = duration[1].split('min')
        mins = int(duration[1][0])
        time_in_secs = time_in_secs + mins*60
    elif 'min' in duration:
        duration = duration.split('min')
        mins = int(duration[0])
        time_in_secs = time_in_secs + mins*60
    time_in_secs -= (0.2*time_in_secs)
    return time_in_secs

def update_prompt(user, progress_cache, current_episode):
    print('I just noticed that you changed the episode. Do you want to update your MAL? [Y/N]')
    y = input().lower()
    if y == 'y' or y == 'yes':
        episode = current_episode-1
        response = update_ep(user, int(progress_cache['anime_details']['mal_id']), episode)
        try:
            if response['status']:
                print('Successfully updated list!')
                time.sleep(2)
                clear()
        except(KeyError):
            print(response)
            time.sleep(5)
    else:
        time.sleep(1)
        clear()

def track(episode_info, progress_cache, user):
    episode_check = 0
    try:
        current_episode = get_episode(episode_info, progress_cache, user)[0]
    except IndexError:
        while True:
            clear()
            print('VLC is not running.')
            time.sleep(2)
            if get_episode(episode_info, progress_cache, user) != []:
                current_episode = get_episode(episode_info, progress_cache, user)[0]
                break
    except Exception as e:
        print(e)
        print('\n(Press Ctrl+C to quit)')
    while True:
        try:
            try:
                if get_episode(episode_info, progress_cache, user)[0] == current_episode:
                    clear()
                    print('Currently watching episode {} of {}'.format(str(current_episode), progress_cache['anime_details']['title']))
                    print('\n(Press Ctrl+C to quit)')
                    raise IOError
                else:
                    current_episode = get_episode(episode_info, progress_cache, user)[0]
                    clear()
                    print('Currently watching episode {} of {}'.format(str(current_episode), progress_cache['anime_details']['title']))
                    print('\n(Press Ctrl+C to quit)')
                    raise IndentationError
            except(IOError):
                time.sleep(5)
            except(IndentationError):
                update_prompt(user, progress_cache, current_episode)
            except IndexError:
                clear()
                print('VLC is not running.')
                if episode_check != current_episode:
                    update_prompt(user, progress_cache, current_episode+1)
                    episode_check = current_episode
                else:
                    pass
                time.sleep(3)
        except IndexError:
            pass
        except KeyboardInterrupt:
            print('\nOmae Wa Mou Shindeiru.')
            sys.exit()