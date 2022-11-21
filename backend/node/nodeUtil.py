import requests

def authenticated_GET(url, node):
    '''
    Given the url to send to the specified node,
    sends a GET request to that url with HTTP Basic Auth
    '''
    res = requests.get(url, auth=(node.username, node.password))
    return res

def authenticated_POST(url, node, data):
    res = requests.post(url, data=data, auth=(node.username, node.password))
    return res




