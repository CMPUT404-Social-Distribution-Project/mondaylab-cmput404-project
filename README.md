# SocialDistribution: a social media app by Team01 
***Created in CMPUT-404 Fall 2022 course***
##  Team Members  
  
| <img src="https://avatars.githubusercontent.com/u/49131259?v=4" width="120">| <img src="https://avatars.githubusercontent.com/u/57372321?v=4" width="120"> | <img src="https://avatars.githubusercontent.com/u/66976914?v=4" width="120"> | <img src="https://avatars.githubusercontent.com/u/77299977?v=4" width="120"> | <img src="https://avatars.githubusercontent.com/u/98789620?v=4" width="120"> |
:---: | :---: | :---: | :---: | :---:
|[happycat33](https://github.com/happycat33)|[jackie174](https://github.com/jackie174)|[TruongGiangPham-1](https://github.com/TruongGiangPham-1)|[rmo1ualberta](https://www.youtube.com/watch?v=dQw4w9WgXcQ)|[em1i](https://github.com/em1i)|

---
### For devs:

Be sure to run this in a virtual environment:
```
virtualenv venv
source venv/bin/activate
```
And install the requirements:
```
pip install -r requirements.txt
```

For front-end devs:
```
cd socialapp
npm install
```

# API Info
#### End Points
#####🔶 - requires authentication with JWT (JSON Web Tokens). Token is given in a HTTP response when author is initially registered.

`/service/auth/register` 
|   Method   | Description | Required Fields | Optional Fields
| ---------- | --------------------| - | - |
| ***POST*** | Registers an author | **displayName:** *max 200 char* <br/> **password:** *min 8 char, max 128 char* | **github:** *in URL format*
<hr style="height: 1px; margin: 0rem 0rem 2rem 0rem;"/>

`/service/auth/login`
|   Method   | Description | Required Fields | Optional Fields |
| ---------- | ------------| --------------- | --------------- |
| ***POST*** | Logs in an author | **displayName:** *max 200 char* <br/> **password:** *min 8 char, max 128 char* | 
<hr style="height: 1px; margin: 0rem 0rem 2rem 0rem;"/>

`/service/auth/refresh`
|   Method   | Description | Required Fields | Optional Fields
| ---------- | --------------------| - | - |
| ***POST*** | Refreshes a token | **refresh:** *the token to be refreshed* 
<hr style="height: 1px; margin: 0rem 0rem 2rem 0rem;"/>

`/service/authors/`
|   Method   | Description | Required Fields | Optional Fields
| ---------- | --------------------| - | - |
| ***GET*** | Retrieves all the authors on the server |  | 
<hr style="height: 1px; margin: 0rem 0rem 2rem 0rem;"/>

`/service/authors/<author_id>/`
|   Method   | Description | Required Fields | Optional Fields
| ---------- | --------------------| - | - |
| ***GET*** | Retrieves the user with UUID specified in <author_id> | | 
| ***POST🔶*** | Updates the user with the all the specified fields | | **host:** where the author is hosted <br/> **displayName:** *max 200 char, must be unique* <br/> **url:** the URL to the author's profile <br/> **github:** URL field <br/> **profileImage:** URL link to author's profile image <br/>
| ***PATCH🔶*** | Partially updates the user with the specified fields | |
<hr style="height: 1px; margin: 0rem 0rem 2rem 0rem;"/>

`/service/authors/<author_id>/posts/`
|   Method   | Description | Required Fields | Optional Fields
| ---------- | --------------------| - | - |
| ***GET*** | Retrieves all the posts of the author with UUID <author_id> | | 
| ***POST🔶*** | Creates a post for author with UUID <author_id>, id auto generated |  | **title:** *max 50 char* <br/> **source:** URL field, the link where the post we got from <br/> **origin:** URL field, the link where the post is originaly from <br/> **description:** *max 300 char* <br/> **contentType:** *max 200 char* \ supported mimetypes: [text/markdown, text/plain, application/base64, image/png:base64, image/jpg:base64] <br/> **content:** the content. <br/> **categories:** list containing the categories <br/> **visibility:** choose from [friends, public] <br/> **unlisted:** *boolean*
<hr style="height: 1px; margin: 0rem 0rem 2rem 0rem;"/>

`/service/authors/<author_id>/posts/<post_id>/`
|   Method   | Description | Required Fields | Optional Fields
| ---------- | --------------------| - | - |
| ***GET*** | Gets the public post of author <author_id >at <post_id> | | 
| ***POST🔶*** | Updates the post <post_uid> from author with UUID <author_id> |  | **title:** *max 50 char* <br/> **source:** URL field, the link where the post we got from <br/> **origin:** URL field, the link where the post is originaly from <br/> **description:** *max 300 char* <br/> **contentType:** *max 200 char* \ supported mimetypes: [text/markdown, text/plain, application/base64, image/png:base64, image/jpg:base64] <br/> **content:** the content. <br/> **categories:** list containing the categories <br/> **visibility:** choose from [friends, public] <br/> **unlisted:** *boolean*
| ***PUT🔶*** | Creates a post for author with UUID <author_id>, id generated from the post_id specified in the request URL. e.g. `PUT http://localhost//service/authors/asgkljg/posts/asd/` generates a post with id=asd. ****NOTE: the ID MUST BE A UUID4!!!**** |  | same as above
| ***DELETE🔶*** | Deletes the post <post_id> from author <author_id> | | 

## References

https://supertokens.com/blog/building-a-login-screen-with-react-and-bootstrap

https://dev.to/koladev/django-rest-authentication-cmh

https://sushil-kamble.medium.com/django-rest-framework-react-authentication-workflow-2022-part-1-a21f22b3f358

https://blog.devgenius.io/django-rest-framework-react-authentication-workflow-2022-part-2-d299b7fef875