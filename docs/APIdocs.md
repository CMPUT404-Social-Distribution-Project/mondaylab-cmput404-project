#### End Points
🔶 - requires authentication with JWT (JSON Web Tokens). Token is given in a HTTP response when author is initially registered.
**NOTE:** Fields with a bracket next to them indicates their default values. If not stated, assume the default will be blank/empty string (this only applies for optional fields, required fields are just that; they cannot be blank) 

`/service/auth/register` 
|   Method   | Description | Required Fields | Optional Fields
| ---------- | --------------------| - | - |
| ***POST*** | Registers an author | **displayName:** *max 200 char* <br/> **password:** *min 8 char, max 128 char* | **github:** *in URL format*  

Example response:
```json
{
    "user": {
        "id": "http://127.0.0.1:8000/authors/8b6448cc-35fe-4069-a3f6-0b49a7e259bc",
        "github": "",
        "host": "http://127.0.0.1:8000/"
    },
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY3MTM5NDQ3OCwiaWF0IjoxNjY3MDc0NDc4LCJqdGkiOiJiYTkxMDU5NWQ4ZTU0YzYxOGVkOGRiYzM2ZDNhNTc4ZSIsInVzZXJfaWQiOiJodHRwOi8vMTI3LjAuMC4xOjgwMDAvYXV0aG9ycy84YjY0NDhjYy0zNWZlLTQwNjktYTNmNi0wYjQ5YTdlMjU5YmMifQ.oSqLFMPRgDRl--yl2qPkEVqTi_Ub4IDo4lTGBI86CO0",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjY3MDg1Mjc4LCJpYXQiOjE2NjcwNzQ0NzgsImp0aSI6IjQwYmRhYzQ5NTkwOTRjOGFiMzkxZDQ2ZmU1MDY3Y2E2IiwidXNlcl9pZCI6Imh0dHA6Ly8xMjcuMC4wLjE6ODAwMC9hdXRob3JzLzhiNjQ0OGNjLTM1ZmUtNDA2OS1hM2Y2LTBiNDlhN2UyNTliYyJ9.R0FJRPynUR_O146woqsmKTCq_u1Ni0hSvCsptvDaARo"
}
```
The "token" field would then be stored and used by the client, by putting the token in the Authorization header of the client's request message:
`Authorization: Bearer <TOKEN_HERE>`
But we note here that the token has a limited lifetime, and the client should check for the expiry time and request for a refresh token when that time has passed.
<hr style="height: 1px; margin: 0rem 0rem 2rem 0rem;"/>

`/service/auth/login`
|   Method   | Description | Required Fields | Optional Fields |
| ---------- | ------------| --------------- | --------------- |
| ***POST*** | Logs in an author | **displayName:** *max 200 char* <br/> **password:** *min 8 char, max 128 char* |  

Example response: 
```json
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY3MTM5NDc1NSwiaWF0IjoxNjY3MDc0NzU1LCJqdGkiOiI3ODkwNDJhZTI5NDk0NDUzYmEwMjFlZDhjMmI2NDlhMCIsInVzZXJfaWQiOiJodHRwOi8vMTI3LjAuMC4xOjgwMDAvYXV0aG9ycy84YjY0NDhjYy0zNWZlLTQwNjktYTNmNi0wYjQ5YTdlMjU5YmMifQ.rcSscEFfW7UtVcGbLNmK9bMJ6QsJAeQIHgtd-el3Ie8",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjY3MDg1NTU1LCJpYXQiOjE2NjcwNzQ3NTUsImp0aSI6IjVkNTZjZjZjNGI2NDRhMWQ5NzA2YTM4ZjA1NDM4OTU1IiwidXNlcl9pZCI6Imh0dHA6Ly8xMjcuMC4wLjE6ODAwMC9hdXRob3JzLzhiNjQ0OGNjLTM1ZmUtNDA2OS1hM2Y2LTBiNDlhN2UyNTliYyJ9.eD30TfT28KZgzlO7rGRPpxe9Uh0DeH1ahZOuuFCT3g0",
    "user": {
        "id": "http://127.0.0.1:8000/authors/8b6448cc-35fe-4069-a3f6-0b49a7e259bc",
        "uuid": "8b6448cc-35fe-4069-a3f6-0b49a7e259bc",
        "host": "http://127.0.0.1:8000/",
        "displayName": "bruh",
        "url": "http://127.0.0.1:8000/authors/8b6448cc-35fe-4069-a3f6-0b49a7e259bc",
        "github": "",
        "profileImage": "",
        "is_active": true,
        "is_superuser": false,
        "type": "author",
        "followers": []
    }
}
```
<hr style="height: 1px; margin: 0rem 0rem 2rem 0rem;"/>

`/service/auth/refresh`
|   Method   | Description | Required Fields | Optional Fields
| ---------- | --------------------| - | - |
| ***POST*** | Refreshes a token | **refresh:** *the refresh token*

Example response:
```json
{
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjY3MDg1NjM2LCJpYXQiOjE2NjcwNzQ0NzgsImp0aSI6ImNlODU1MGMyNDQ4NDRmNjY4MDIyZmI5YzRhMWMxOGZmIiwidXNlcl9pZCI6Imh0dHA6Ly8xMjcuMC4wLjE6ODAwMC9hdXRob3JzLzhiNjQ0OGNjLTM1ZmUtNDA2OS1hM2Y2LTBiNDlhN2UyNTliYyJ9.ZpELUK59oPGAb545oIBxz3nyGNFWAWh6Hsd8zZUk2m0",
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY3MTM5NDgzNiwiaWF0IjoxNjY3MDc0ODM2LCJqdGkiOiI0MmFhMzA3MjY2MjE0NjNjYjBhY2E0NTc4NTNiMGM1ZCIsInVzZXJfaWQiOiJodHRwOi8vMTI3LjAuMC4xOjgwMDAvYXV0aG9ycy84YjY0NDhjYy0zNWZlLTQwNjktYTNmNi0wYjQ5YTdlMjU5YmMifQ.Q-5J7oN9wNSTN3uf8CuLEMPoBy1bWxB823XD-keK4Tw"
}
```
Note here that the field `refresh` should be sent through the body, and is the token that is from the 'refresh' field received when registering/logging in, and NOT the token from the access/token field. 
<hr style="height: 1px; margin: 0rem 0rem 2rem 0rem;"/>

`/service/authors/`
|   Method   | Description | Required Fields | Optional Fields
| ---------- | --------------------| - | - |
| ***GET***(paginated) | Retrieves all the authors on the server |  | 

Example response:
```json
{
    "type": "authors",
    "items": [
        {
            "id": "http://127.0.0.1:8000/authors/d5feb01d-934b-4d7f-9455-11596efc8fa8",
            "uuid": "d5feb01d-934b-4d7f-9455-11596efc8fa8",
            "host": "http://127.0.0.1:8000/",
            "displayName": "ray",
            "url": "http://127.0.0.1:8000/authors/d5feb01d-934b-4d7f-9455-11596efc8fa8",
            "github": "",
            "profileImage": "",
            "is_active": true,
            "is_superuser": true,
            "type": "author",
            "followers": []
        },
        {
            "id": "http://127.0.0.1:8000/authors/8b6448cc-35fe-4069-a3f6-0b49a7e259bc",
            "uuid": "8b6448cc-35fe-4069-a3f6-0b49a7e259bc",
            "host": "http://127.0.0.1:8000/",
            "displayName": "bruh",
            "url": "http://127.0.0.1:8000/authors/8b6448cc-35fe-4069-a3f6-0b49a7e259bc",
            "github": "",
            "profileImage": "",
            "is_active": true,
            "is_superuser": false,
            "type": "author",
            "followers": []
        }
    ]
}
```
<hr style="height: 1px; margin: 0rem 0rem 2rem 0rem;"/>

`/service/authors/<author_id>/`
|   Method   | Description | Required Fields | Optional Fields
| ---------- | --------------------| - | - |
| ***GET*** | Retrieves the user with UUID specified in <author_id> | | 
| ***POST🔶*** | Updates the user with the all the specified fields | | **host:** where the author is hosted <br/> **displayName:** *max 200 char, must be unique* <br/> **url:** the URL to the author's profile <br/> **github:** URL field <br/> **profileImage:** URL link to author's profile image <br/>
| ***PATCH🔶*** | Partially updates the user with the specified fields | |

Example response:
```json
{
    "id": "http://127.0.0.1:8000/authors/d5feb01d-934b-4d7f-9455-11596efc8fa8",
    "uuid": "d5feb01d-934b-4d7f-9455-11596efc8fa8",
    "host": "http://127.0.0.1:8000/",
    "displayName": "ray",
    "url": "http://127.0.0.1:8000/authors/d5feb01d-934b-4d7f-9455-11596efc8fa8",
    "github": "",
    "profileImage": "",
    "is_active": true,
    "is_superuser": true,
    "type": "author",
    "followers": []
}
```
<hr style="height: 1px; margin: 0rem 0rem 2rem 0rem;"/>

`/service/authors/<author_id>/posts/`
|   Method   | Description | Required Fields | Optional Fields
| ---------- | --------------------| - | - |
| ***GET*** | Retrieves all the posts of the author with UUID <author_id> | | 
| ***POST🔶*** | Creates a post for author with UUID <author_id>, id auto generated | **contentType:** *max 200 char* \ supported mimetypes: [text/markdown, text/plain, application/base64, image/png:base64, image/jpg:base64] <br/> **visibility:** choose from [FRIENDS, PUBLIC] | **title:** *max 50 char* <br/> **source:** URL field, the link where the post we got from <br/> **origin:** URL field, the link where the post is originally from <br/> **description:** *max 300 char* <br/> **content:** the content. <br/> **categories:** list containing the categories <br/> **unlisted [default: False]:** *boolean*

Example response:
```json
{
    "type": "posts",
    "items": [
        {
            "uuid": "9fc6ae0b-c0a6-4af5-bf26-41f16c45d1d0",
            "type": "post",
            "title": "A test post!",
            "id": "http://127.0.0.1:8000/authors/d5feb01d-934b-4d7f-9455-11596efc8fa8/posts/9fc6ae0b-c0a6-4af5-bf26-41f16c45d1d0",
            "source": "http://127.0.0.1:8000/authors/d5feb01d-934b-4d7f-9455-11596efc8fa8/posts/9fc6ae0b-c0a6-4af5-bf26-41f16c45d1d0",
            "origin": "http://127.0.0.1:8000/authors/d5feb01d-934b-4d7f-9455-11596efc8fa8/posts/9fc6ae0b-c0a6-4af5-bf26-41f16c45d1d0",
            "description": "",
            "contentType": "text/plain",
            "content": "There's some stuff here.",
            "categories": "",
            "count": 0,
            "comments": "http://127.0.0.1:8000/authors/d5feb01d-934b-4d7f-9455-11596efc8fa8/posts/9fc6ae0b-c0a6-4af5-bf26-41f16c45d1d0/comments",
            "published": "2022-10-29T20:44:19.604440Z",
            "visibility": "PUBLIC",
            "unlisted": false,
            "author": {
                "id": "http://127.0.0.1:8000/authors/d5feb01d-934b-4d7f-9455-11596efc8fa8",
                "uuid": "d5feb01d-934b-4d7f-9455-11596efc8fa8",
                "host": "http://127.0.0.1:8000/",
                "displayName": "ray",
                "url": "http://127.0.0.1:8000/authors/d5feb01d-934b-4d7f-9455-11596efc8fa8",
                "github": "",
                "profileImage": "",
                "type": "author"
            },
            "commentSrc": {
                "comments": [],
                "type": "",
                "id": "",
                "contentType": "",
                "published": "",
                "comment": "",
                "author": null
            }
        }
    ]
}
```
<hr style="height: 1px; margin: 0rem 0rem 2rem 0rem;"/>

`/service/authors/<author_id>/posts/<post_id>`
|   Method   | Description | Required Fields | Optional Fields
| ---------- | --------------------| - | - |
| ***GET*** | Gets the public post of author <author_id >at <post_id> | | 
| ***POST🔶*** | Updates the post <post_uid> from author with UUID <author_id> |   **title:** *max 50 char* <br/> **source:** URL field, the link where the post we got from <br/> **origin:** URL field, the link where the post is originaly from <br/> **description:** *max 300 char* <br/>  **content:** the content. <br/> **categories:** list containing the categories <br/> **contentType:** *max 200 char* \ supported mimetypes: [text/markdown, text/plain, application/base64, image/png:base64, image/jpg:base64] <br>**visibility:** choose from [FRIENDS, PUBLIC] <br/> **unlisted:** *boolean* |
| ***PATCH🔶*** | Partially updates the post <post_uid> from author with UUID <author_id> | |   **title:** *max 50 char* <br/> **source:** URL field, the link where the post we got from <br/> **origin:** URL field, the link where the post is originaly from <br/> **description:** *max 300 char* <br/>  **content:** the content. <br/> **categories:** list containing the categories <br/> **contentType:** *max 200 char* \ supported mimetypes: [text/markdown, text/plain, application/base64, image/png:base64, image/jpg:base64] <br/>**visibility:** choose from [FRIENDS, PUBLIC] <br/> **unlisted:** *boolean* |
| ***PUT🔶*** | Creates a post for author with UUID <author_id>, id generated from the post_id specified in the request URL. e.g. `PUT http://localhost//service/authors/asgkljg/posts/asd/` generates a post with id=asd. ****NOTE: the ID MUST BE A UUID4!!!**** |  | same as above
| ***DELETE🔶*** | Deletes the post <post_id> from author <author_id> | | 

Example response:
```json
{
    "uuid": "9fc6ae0b-c0a6-4af5-bf26-41f16c45d1d0",
    "type": "post",
    "title": "A test post!",
    "id": "http://127.0.0.1:8000/authors/d5feb01d-934b-4d7f-9455-11596efc8fa8/posts/9fc6ae0b-c0a6-4af5-bf26-41f16c45d1d0",
    "source": "http://127.0.0.1:8000/authors/d5feb01d-934b-4d7f-9455-11596efc8fa8/posts/9fc6ae0b-c0a6-4af5-bf26-41f16c45d1d0",
    "origin": "http://127.0.0.1:8000/authors/d5feb01d-934b-4d7f-9455-11596efc8fa8/posts/9fc6ae0b-c0a6-4af5-bf26-41f16c45d1d0",
    "description": "",
    "contentType": "text/plain",
    "content": "There's some stuff here.",
    "categories": "",
    "count": 0,
    "comments": "http://127.0.0.1:8000/authors/d5feb01d-934b-4d7f-9455-11596efc8fa8/posts/9fc6ae0b-c0a6-4af5-bf26-41f16c45d1d0/comments",
    "published": "2022-10-29T20:44:19.604440Z",
    "visibility": "PUBLIC",
    "unlisted": false,
    "author": {
        "id": "http://127.0.0.1:8000/authors/d5feb01d-934b-4d7f-9455-11596efc8fa8",
        "uuid": "d5feb01d-934b-4d7f-9455-11596efc8fa8",
        "host": "http://127.0.0.1:8000/",
        "displayName": "ray",
        "url": "http://127.0.0.1:8000/authors/d5feb01d-934b-4d7f-9455-11596efc8fa8",
        "github": "",
        "profileImage": "",
        "type": "author"
    },
    "commentSrc": {
        "comments": [],
        "type": "",
        "id": "",
        "contentType": "",
        "published": "",
        "comment": "",
        "author": null
    }
}
```
<hr style="height: 1px; margin: 0rem 0rem 2rem 0rem;"/>

`/service/authors/<author_id>/posts/<post_id>/comments/`
|   Method   | Description | Required Fields | Optional Fields
| ---------- | --------------------| - | - |
| ***GET***(paginated) | Gets the comments of post <post_id> of author <author_id> | | 
| ***POST🔶*** | Adds a comment to post <post_id> of author <author_id > | | **comment:** *max 200 char*  

Example response:
```json
{
    "type": "comments",
    "page": 1,
    "size": 5,
    "post": "http://127.0.0.1:8000/authors/d5feb01d-934b-4d7f-9455-11596efc8fa8/posts/9fc6ae0b-c0a6-4af5-bf26-41f16c45d1d0",
    "id": "http://127.0.0.1:8000/authors/d5feb01d-934b-4d7f-9455-11596efc8fa8/posts/9fc6ae0b-c0a6-4af5-bf26-41f16c45d1d0/comments",
    "comments": [
        {
            "uuid": "9c0362a5-4627-42ea-b0a6-8e065a8bbb72",
            "author": {
                "id": "http://127.0.0.1:8000/authors/d5feb01d-934b-4d7f-9455-11596efc8fa8",
                "uuid": "d5feb01d-934b-4d7f-9455-11596efc8fa8",
                "host": "http://127.0.0.1:8000/",
                "displayName": "ray",
                "url": "http://127.0.0.1:8000/authors/d5feb01d-934b-4d7f-9455-11596efc8fa8",
                "github": "",
                "profileImage": "https://media.tenor.com/OpZ2m8MSSLwAAAAC/mob-psycho-shy.gif",
                "type": "author"
            },
            "type": "comment",
            "id": "http://127.0.0.1:8000/authors/d5feb01d-934b-4d7f-9455-11596efc8fa8/posts/9fc6ae0b-c0a6-4af5-bf26-41f16c45d1d0/comments/9c0362a5-4627-42ea-b0a6-8e065a8bbb72",
            "contentType": "text/markdown",
            "published": "2022-10-29 00:00:00",
            "comment": "pls"
        }
    ]
}
```
<hr style="height: 1px; margin: 0rem 0rem 2rem 0rem;"/>

`/service/authors/<author_id>/posts/<post_id>/likes`
|   Method   | Description | Required Fields | Optional Fields
| ---------- | --------------------| - | - |
| ***GET*** | Gets the list of likes from other authors of post <post_id> of author <author_id> | | 

Example response:
```json
{
    "type": "likes",
    "items": [
        {
            "summary": "bruh likes your post",
            "type": "Like",
            "author": {
                "id": "http://127.0.0.1:8000/authors/8b6448cc-35fe-4069-a3f6-0b49a7e259bc",
                "uuid": "8b6448cc-35fe-4069-a3f6-0b49a7e259bc",
                "host": "http://127.0.0.1:8000/",
                "displayName": "bruh",
                "url": "http://127.0.0.1:8000/authors/8b6448cc-35fe-4069-a3f6-0b49a7e259bc",
                "github": "",
                "profileImage": "",
                "type": "author"
            },
            "object": "http://127.0.0.1:8000/authors/d5feb01d-934b-4d7f-9455-11596efc8fa8/posts/9fc6ae0b-c0a6-4af5-bf26-41f16c45d1d0"
        }
    ]
}
```
<hr style="height: 1px; margin: 0rem 0rem 2rem 0rem;"/>

`/service/authors/<author_id>/posts/<post_id>/comments/<comment_id>/likes`
|   Method   | Description | Required Fields | Optional Fields
| ---------- | --------------------| - | - |
| ***GET*** | Gets the list of likes from other authors of <author_id> post <post_id> on comment <comment_id> | | 

Example response:
<hr style="height: 1px; margin: 0rem 0rem 2rem 0rem;"/>

`/service/authors/<author_id>/liked`
|   Method   | Description | Required Fields | Optional Fields
| ---------- | --------------------| - | - |
| ***GET*** | Lists the like objects of public posts that <author_id> liked  | | 

Example response:
```json
{
    "type": "liked",
    "items": [
        {
            "summary": "bruh likes your post",
            "type": "Like",
            "object": "http://127.0.0.1:8000/authors/d5feb01d-934b-4d7f-9455-11596efc8fa8/posts/9fc6ae0b-c0a6-4af5-bf26-41f16c45d1d0"
        }
    ]
}
```
<hr style="height: 1px; margin: 0rem 0rem 2rem 0rem;"/>

`/service/authors/<author_id>/followers/`
|   Method   | Description | Required Fields | Optional Fields
| ---------- | --------------------| - | - |
| ***GET*** | Gets the followers of author <author_id> | | 

Example response:
```json
{
    "type": "followers",
    "items": [
        {
            "type": "author",
            "id": "http://127.0.0.1:8000/authors/8b6448cc-35fe-4069-a3f6-0b49a7e259bc",
            "uuid": "8b6448cc-35fe-4069-a3f6-0b49a7e259bc",
            "url": "http://127.0.0.1:8000/authors/8b6448cc-35fe-4069-a3f6-0b49a7e259bc",
            "host": "http://127.0.0.1:8000/",
            "displayName": "bruh",
            "github": "",
            "profileImage": ""
        }
    ]
}
```
<hr style="height: 1px; margin: 0rem 0rem 2rem 0rem;"/>

`/service/authors/<author_id>/followers/<foreign_author_id>`
|   Method   | Description | Required Fields | Optional Fields
| ---------- | --------------------| - | - |
| ***GET*** | Checks if <foreign_author_id> is friends with <author_id>. Returns a Boolean. | | 
| ***PUT🔶*** | Adds <foreign_author_id> as a follower of <author_id>.  | | 
| ***DELETE🔶*** | Removes <foreign_author_id> from the followers list of <author_id>. **NOTE:** Only <foreign_author_id> needs to be authorized to use this method. This is so then <foreign_author_id> can unfollow without needing <author_id>'s permission. | | 
<hr style="height: 1px; margin: 0rem 0rem 2rem 0rem;"/>

`/service/authors/<author_id>/inbox/`
|   Method   | Description | Required Fields | Optional Fields
| ---------- | --------------------| - | - |
| ***GET🔶*** | Gets the inbox of author <author_id> | | 
| ***POST*** | Sends an object to the inbox of author <author_id> <br> **[OBJECTS MUST FOLLOW THEIR FORMATS AS SEEN IN PROJECT SPECS.](inbox_objects.org)** | | 
| ***DELETE🔶*** | Clears the inbox of author <author_id> | | 

Example response:
```json
{
    "type": "inbox",
    "author": "http://127.0.0.1:8000/authors/d5feb01d-934b-4d7f-9455-11596efc8fa8",
    "items": [
        {
            "summary": "bruh likes your post",
            "type": "Like",
            "author": {
                "id": "http://127.0.0.1:8000/authors/8b6448cc-35fe-4069-a3f6-0b49a7e259bc",
                "uuid": "8b6448cc-35fe-4069-a3f6-0b49a7e259bc",
                "host": "http://127.0.0.1:8000/",
                "displayName": "bruh",
                "url": "http://127.0.0.1:8000/authors/8b6448cc-35fe-4069-a3f6-0b49a7e259bc",
                "github": "",
                "profileImage": "",
                "type": "author"
            },
            "object": "http://127.0.0.1:8000/authors/d5feb01d-934b-4d7f-9455-11596efc8fa8/posts/9fc6ae0b-c0a6-4af5-bf26-41f16c45d1d0"
        }
    ]
}
```
#### [Object types and their respective formats](inbox_objects.org)

<hr style="height: 1px; margin: 0rem 0rem 2rem 0rem;"/>

`/service/authors/<author_id>/friends/`
|   Method   | Description | Required Fields | Optional Fields
| ---------- | --------------------| - | - |
| ***GET*** | Gets the friends list of author <author_id> | | 

Example response:
```json
{
    "type": "friends",
    "items": [
        {
            "id": "http://127.0.0.1:8000/authors/8b6448cc-35fe-4069-a3f6-0b49a7e259bc",
            "uuid": "8b6448cc-35fe-4069-a3f6-0b49a7e259bc",
            "host": "http://127.0.0.1:8000/",
            "displayName": "bruh",
            "url": "http://127.0.0.1:8000/authors/8b6448cc-35fe-4069-a3f6-0b49a7e259bc",
            "github": "",
            "profileImage": "",
            "type": "author"
        }
    ]
}
```
<hr style="height: 1px; margin: 0rem 0rem 2rem 0rem;"/>

`/service/authors/<author_id>/friends/<foreign_author_id>`
|   Method   | Description | Required Fields | Optional Fields
| ---------- | --------------------| - | - |
| ***GET*** | Checks if <foreign_author_id> is a friend of <author_id><br> Returns a boolean | | 

<hr style="height: 1px; margin: 0rem 0rem 2rem 0rem;"/>

