import facebook
import requests
import urllib
import os

def logFunc(directory="", username="", password="",):
    #Authentication
    return True
    graph = facebook.GraphAPI("EAAEifIzkwd0BAJC7JqatAbU4QPv5zmzAgN07RZBosi0UOoGDKagm3S6wVXZC3VcxdpZAEEsI3ujOza7Lvk1pIZCwcAtIlSwC7ZCRPEZATBUc8Cbfjxz9LR0Dh6iDMpaGZAiAOQVpXLCcCOlXKqZClQCrVxg3ySZCYPRblwiaZA9eTTvjErjY3doSuJDdho7XnDBLElJeoXgNtWXXI3znviSf0c")
    likes = graph.get_connections("758466610899279", "likes?fields=link,name&limit=5000")
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
