
export function extractAuthorUUID(id) {
    // Given the author's id field, splits the id to extract the UUID
    const splitArray = id.split("authors/");
    let UUID = splitArray[1];
    if (id.slice(-1) === '/') {
        UUID = UUID.slice(0, -1);   //remove end slash
    }
    return UUID
}

export function extractPostUUID(id) {
    // Given the post's id field, splits the id to extract the UUID
    const splitArray = id.split("posts/");
    let UUID = splitArray[1];
    if (id.slice(-1) === '/') {
        UUID = UUID.slice(0, -1);   //remove end slash
    }
    return UUID
}

export function authorHostIsOurs(host) {
    // Checks if the given host field of the author is our host
    return "http://localhost:8000/".includes(host) || 
    "http://127.0.0.1:8000/".includes(host) ||
    "https://cs404-project.herokuapp.com/".includes(host)
}
