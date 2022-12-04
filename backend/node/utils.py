import requests
from .models import Node

# NOTE: Used for querying with objects. E.g. Author.objects.get(host__in=our_hosts) returns authors from our host.
# TODO: Add "https://cs404-project.herokuapp.com/service/" later
our_hosts_api = ["http://localhost:8000/service/","http://testserver/service/" ]
our_hosts = ["http://localhost:8000/", "http://testserver"]


def authenticated_GET(url, node):
    '''
    Given the url to send to the specified node,
    sends a GET request to that url with HTTP Basic Auth
    '''
    try:
        res = requests.get(url, auth=(node.username, node.password), timeout=5)
    except Exception as e:
        print(f"authenticated_GET: Failed to fetch to {url} with {node.username}:{node.password}", e)
        return e
    return res

def authenticated_GET_host(endpoint, host, author_url=None):
    '''
    Given the endpoint to send to the specified node,
    sends a GET request to that url with HTTP Basic Auth
    Example:
    endpoint = "authors/<author_id>"
    host = "localhost:8000"
    '''
    node = Node.objects.get(host__contains=host)
    custom_header = {}
    # if author_url:
    #     custom_header = {'x-request-author': author_url}
    try:
        res = requests.get(f"{node.host}{endpoint}", auth=(node.username, node.password), headers=custom_header, timeout=5)
    except Exception as e:
        print(f"authenticated_GET_host: Failed to fetch to {node.host}{endpoint}.", e)
        return e
    return res

def authenticated_POST(url, node, data):
    res = requests.post(url, json=data, auth=(node.username, node.password))
    return res

def getNodeRemoteAuthors(node):
    # Gets a single node's authors

    node_authors_endpoint = f"{node.host}authors/"
    res = authenticated_GET(node_authors_endpoint, node)
    if isinstance(res, str):
        print(f"getNodeRemoteAuthors: Failed with error: {res}")
        return []
    if (res.status_code == 200):
        return res.json()["items"]
    else:
        return []
