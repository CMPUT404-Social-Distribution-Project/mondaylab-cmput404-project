import requests
from .models import Node

# TODO: Add "https://cs404-project.herokuapp.com/service/" later
our_hosts_api = ["https://cs404-project.herokuapp.com/service/"]
our_hosts = ["https://cs404-project.herokuapp.com/"]


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

def getRemoteAuthors():
    
    all_nodes = Node.objects.exclude(host__in=our_hosts_api)
    all_nodes_authors = list()
    for node in all_nodes:
        node_authors_endpoint = f"{node.host}authors/"
        res = authenticated_GET(node_authors_endpoint, node)
        if (res.status_code == 200):
            all_nodes_authors.extend(res.json()["items"])

    return all_nodes_authors

def getNodeRemoteAuthors(node):
    # Gets a single node's authors

    node_authors_endpoint = f"{node.host}authors/"
    res = authenticated_GET(node_authors_endpoint, node)
    print(f"getNodeRemoteAuthors: Failed with res {res.status_code}:{res.content}")
    if (res.status_code == 200):
        return res.json()["items"]
    else:
        return []
