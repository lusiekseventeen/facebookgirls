import facebook
import urllib
import os

def logFunc(username, password, directory):
    #TODO Wyłuskać Access token z hasła i użytkownika.
    graph = facebook.GraphAPI("<Access Token from Developers page>")
    likes = graph.get_connections("<node id>", "likes?fields=link,name&limit=5000")
    for i in range(0, len(likes["data"])):
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
        urllib.request.urlretrieve(pic["data"]["url"], "directory" + nodename + ".jpg")