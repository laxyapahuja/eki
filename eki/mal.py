import malupdate as mal
import requests

from eki.login import login

def update_ep(user, mal_id, episode):
    return mal.User.updateList(user['access_token'], mal_id,{
            "num_watched_episodes": episode, "status":"watching"
        })

def update_status(user, mal_id, status):
    mal.User.updateList(user['access_token'], mal_id,
        {
            "status": status
        })

    