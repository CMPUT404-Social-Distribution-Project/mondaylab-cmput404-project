
export function extractAuthorUUID(id) {
    // Given the author's id field, splits the id to extract the UUID
    const splitArray = id.split("authors/");
    let UUID = splitArray[1];
    if (id.slice(-1) === '/') {
        UUID = UUID.slice(0, -1);   //remove end slash
    }
    return UUID.replace('-','');
}

export function extractPostUUID(id) {
    // Given the post's id field, splits the id to extract the UUID
    const splitArray = id.split("posts/");
    let UUID = splitArray[1];
    if (id.slice(-1) === '/') {
        UUID = UUID.slice(0, -1);   //remove end slash
    }
    return UUID.replace('-','');
}

export function authorHostIsOurs(host) {
    // Checks if the given host field of the author is our host
    // TODO: uncomment out last line once we connect with other nodes
    return "https://cs404-project.herokuapp.com/".includes(host)
}

export function b64EncodeCredentials(username, password) {
    const b64Credentials = btoa(`${username}:${password}`)
    return b64Credentials;
}

export function createNodeObject(response, author) {
    // given a response object from GETting to the /node/ 
    // endpoint and the author's host field,
    // creates the node object with the authorization headers
    let node = {...response.data, headers:{}};
    if (!authorHostIsOurs(author.host)) {
      // Post author's host is a remote host (not ours), add in HTTP Basic auth
      const authHeader = `Basic ${b64EncodeCredentials(response.data.username, response.data.password)}`;
      node = {...node, headers: {'Authorization': authHeader}};
      // TODO: Add 'Request-Author': author.id to headers later
    }
    
    return node;
}

export function removeDashes(uuid) {
    return uuid.replace(/-/g,'');
}

export function isValidHTTPUrl(string) {
    let url;
    try {
        url = new URL(string);
      } catch (_) {
        return false;
      }
    return url.protocol === "http:" || url.protocol === "https:";
}

export const emptyNode = {headers: {}};
