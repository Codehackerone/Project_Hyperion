# query ="search despacito in youtube"
import os
import socket
import requests


def sanitize_query(text, query):
    arrquery = query.lower().split()
    if 'in' in arrquery and text == arrquery[arrquery.index("in") + 1]:
        arrquery.remove("in")
    if text in arrquery:
        arrquery.remove(text)
    if "search" in arrquery:
        arrquery.remove("search")
    elif "open" in arrquery:
        arrquery.remove("open")
    query = " ".join(arrquery)
    return query


def getLocation():
    hostname = socket.gethostname()
    ip = str(socket.gethostbyname(hostname))
    complete_url = "http://api.ipstack.com/" + ip + "?access_key=" + "e50e53c71caa1da0d6a012266370b975"
    response = requests.get(complete_url)
    x = response.json()
    latitude = x['latitude']
    longitude = x['longitude']
    return (ip,latitude, longitude,complete_url)


print(getLocation())