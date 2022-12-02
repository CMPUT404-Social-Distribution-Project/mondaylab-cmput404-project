
export function extractAuthorUUID(id) {
    // Given the author's id field, splits the id to extract the UUID
    const splitArray = id.split("authors/");
    let UUID = splitArray[1];
    if (id.slice(-1) === '/') {
        UUID = UUID.slice(0, -1);   //remove end slash
    }
    return UUID;
}

export function extractPostUUID(id) {
    // Given the post's id field, splits the id to extract the UUID
    const splitArray = id.split("posts/");
    let UUID = splitArray[1];
    if (id.slice(-1) === '/') {
        UUID = UUID.slice(0, -1);   //remove end slash
    }
    return UUID;
}

export function authorHostIsOurs(host) {
    // Checks if the given host field of the author is our host
    // TODO: uncomment out last line once we connect with other nodes
    return "http://localhost:8000/".includes(host) || 
    "http://127.0.0.1:8000/".includes(host) 
    // || "https://cs404-project.herokuapp.com/".includes(host)
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

export function urlContainsOurHost(url) {
    return url.includes("localhost") || url.includes("cs404-project.heroku.app.com");
}
