import facebook
from urllib.request import urlretrieve
import os
import requests
import pyquery


class Girl():
    id = 0
    name = ""
    photo_url = ""

    def __init__(self, id, name, photo_url):
        self.id = id
        self.name = name
        self.photo_url = photo_url


def login(session, email, password, array):
    response = session.get('https://m.facebook.com')
    response = session.post('https://m.facebook.com/login.php', data={
        'email': email,
        'pass': password
    }, allow_redirects=False)
    if 'c_user' not in response.cookies:
        return False
    else:
        homepage_resp = session.get('https://m.facebook.com/home.php')
        dom = pyquery.PyQuery(homepage_resp.text.encode('utf8'))
        fb_dtsg = dom('input[name="fb_dtsg"]').val()
        user_id = response.cookies['c_user']
        xs = response.cookies['xs']
        payload = {'grant_type': 'client_credentials', 'client_id': "2030671310550069", 'client_secret': "a497dfc6e769365ab08b93999c3ed76e"}
        file = requests.post('https://graph.facebook.com/oauth/access_token?', params=payload)
        token = file.json()['access_token']
        graph = facebook.GraphAPI(token)
        friends = graph.get_connections(user_id, "friends")
        number = 0
        for i in range(0, len(friends["data"])):
            number += 1
            nodeid = friends["data"][i]["id"]
            nodename = friends["data"][i]["name"]
            nodelink = friends["data"][i]["link"]
            username = nodelink[25:]
            check = (username[:7])
            if (check == "profile"):
                continue
            pic = graph.get_connections(nodeid, "picture?height=9000&redirect=false")
            new = Girl(id=number, name=nodename, photo_url=pic["data"]["url"])
            array.append(new)
        return True



