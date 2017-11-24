import facebook
import requests
import urllib
import os


def get_fb_token(app_id, app_secret):
    payload = {'grant_type': 'client_credentials', 'client_id': app_id, 'client_secret': app_secret}
    file = requests.post('https://graph.facebook.com/oauth/access_token?', params=payload)
    result = file.text.split("=")[1]
    return result

def logFunc(directory="", username="", password="",):
    #Authentication
    token = get_fb_token("319393311801821", "90c63fc2e6a9ecb5dde0a4e861499f6f")
    graph = facebook.GraphAPI(token)
    likes = graph.get_connections("319393311801821", "likes?fields=link,name&limit=5000")
    number = 0
    for i in range(0, len(likes["data"])):
        number += 1
        nodeid = likes["data"][i]["id"]
        nodename = likes["data"][i]["name"]
        nodelink = likes["data"][i]["link"]
        username = nodelink[25:]
        check = (username[:7])
        if (check == "profile"):
            continue
        if (os.path.exists(directory + nodename + ".jpg")):
            continue
        pic = graph.get_connections(username, "picture?height=9000&redirect=false")
        urllib.request.urlretrieve(pic["data"]["url"], "directory" + number + ".jpg")
    return True
