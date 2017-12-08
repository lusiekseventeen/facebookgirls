import sklearn
import pandas
import numpy
import urllib3


def train(classificator, girls, ok):
    http = urllib3.PoolManager()
    for girl in girls:
        r = http.request('GET', girl.photo_url)
    return


def get_prediction(classificator, girl):
    return False