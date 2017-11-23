import facebook
import urllib
import os

def logFunc(directory, username="", password="",):
    graph = facebook.GraphAPI("EAACEdEose0cBAIkEnFiZAFVKdQSqkiLlT9jZC6p8k870TQwXCZAFNe4hfyK3yifdfOpBFUSLRMqBBRV19vIihRDRMgZA32eelZBZCACn8X4CveFvKBSd8QP1D3mK1O2ZCxXL85cJXZC3s1P4EPp0jdadbzqZBUjUAEVmUGBeKT5eYPfJ9LVadFyH2XOxAvLHEHa2M6CfiKKp6kEH5ksXoASi8")
    likes = graph.get_connections("2030671310550069", "likes?fields=link,name&limit=5000")
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