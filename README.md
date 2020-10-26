# Casting-Agency
Capstone project for Udacity Full Stack Web Developer Nanodegree
# Capstone Project - Casting Agency

This is the capstone project for the Udacity Full Stack Nanodegree program. 
This API allows authenticated users to view, edit, add, and delete actors and movies from the server

Heroku URL: https://secure-headland-16470.herokuapp.com/
Heroku git url: https://git.heroku.com/secure-headland-16470.git

##Tokens that can be used for API testing (generated 10/25/2020 at 7:24PM PST):
```bash
CASTING_ASSISTANT = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InFZQmgyLWx0SHlZLUVzYXRXRGF3NSJ9.eyJpc3MiOiJodHRwczovL2Z1bGwtc3RhY2stMjAyMC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWY0ODVhMTI5YzUxMDYwMDZkZTE3NDI5IiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTYwMzY3ODkyMiwiZXhwIjoxNjAzNzY1MzIyLCJhenAiOiJzVEpHNWlWTEE4dHg4bG9ldDc1SnJLWXBUQm1XVGV0WSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.U041BxvsOLfwhNxyeA2e9SKr17xDvAmJdJYpJJAMQk_pXIMM0X689hvPPQIUcAEfbWZ59zsWsWj-CA8LoDJN23xRAwMyiYTNCaI53YG-99iUHqundIZahwoAqbGq9sPqMZOALowk-DDmeSGLxbiY-yo-YdQj4bsMIMh-HsnkZWRndKts8IFCq3OMPS8HqXe8SRmljBVCillyJDvaFpUyjvn-tF8XIGHi9uAq5qw1Lm3qH2-JNcc0WrIu-scrhNEdLwsGN0YT9KiH1XuvFT6gbRHr9CaBHOastGgPufslpWRfCsBIYj_Ztp4-0mSmKSk0tJ8waPbBdLnJ4DzFRjCvPw'                    

CASTING_DIRECTOR = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InFZQmgyLWx0SHlZLUVzYXRXRGF3NSJ9.eyJpc3MiOiJodHRwczovL2Z1bGwtc3RhY2stMjAyMC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWY0NDg4ODFjNjQ3OGIwMDY3ZDgwZTEwIiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTYwMzY3ODk1OCwiZXhwIjoxNjAzNzY1MzU4LCJhenAiOiJzVEpHNWlWTEE4dHg4bG9ldDc1SnJLWXBUQm1XVGV0WSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiXX0.O_eHP83sJTN1s6odg5LNYslXQF2sI7_BDFe3JYMFrrxLGpLJ7RGuFJrEiS3-Ct7QKKW5rLjygoflJ4TlFtujVXtMecs79eNZah-OsfBQIXPxksUY6zvvRidyxoy1L17D5mB08lqeYdaVuwPWjGSyoSkY_4yIiL27hpv9WFgw4BrCe8_6lwfPDsG8lVfqIoE9fhG7cjGPbI1CWbCxFIoQNdKQ9xXZKtj8oSgjGwTsOi1hpshja6DreUxK00PuGbQrqnLTxqfwccq2aMPBkrY2KOYxuFy_khCNAYwfJh16eDore_PZ7tHHZ_ppgapsWD9I-O6yy4ILhnsX1PN54TPRkg'

EXECUTIVE_PRODUCER = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InFZQmgyLWx0SHlZLUVzYXRXRGF3NSJ9.eyJpc3MiOiJodHRwczovL2Z1bGwtc3RhY2stMjAyMC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWY5NDc0OTllN2JmNTUwMDZmZGZhNmE2IiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTYwMzY3ODg3NiwiZXhwIjoxNjAzNzY1Mjc2LCJhenAiOiJzVEpHNWlWTEE4dHg4bG9ldDc1SnJLWXBUQm1XVGV0WSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.FQYCdQ5PdLBZb_N46gHWb_zaxuZThn1Nxt-3Zkig4ZPoSxCQcbBNT3mOPEHLe6qsqR_0CfFIvVZ4Xv-rRo0auY54Zsg0qeUTdMXweiF3akJJ0dWGbV5LSvrdj91_yviJ5R4VFZtSOWdOrtlC3G2z-HUNuaFSwLsfnx1Li1BqqpHyUUi41eD4koYRWixS-xP9C9lWH9FK2ulzb-gXOqq6eggSaDXhgv6HqFJE0iuECfQw4ABgQkpnTSCvEbofIgqoN1P7KMLzOOJhL52j0_2klVoFB-PQsC2U_0BVK88UeUqX_DI7DXPCxqpRU8T8cJJHDe6jAn59j5GkKm_ZDJNcRA'
```

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

I recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once the virtual environment is setup and running, install dependencies by navigating to the working project directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM used to handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 


- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Running the server

From within the directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=app.py
flask run
```
## Authentication

### Casting Assistant
Can view actors and movies

#### Permissions:
```bash
get:actors | get:movies
```

### Casting Director
All permissions of Casting Assistant, plus Add or delete an actor from the databse and modify an actor or movie

#### Permissions:
```bash
get:actors    | get:movies 
delete:actors | post:actors
patch:actors  | patch:movies
```

### Executive Producer
All permissions of Casting director plus ability to add or delete a movie from the database

#### Permissions:
```bash
get:actors    | get:movies 
delete:actors | delete:movies 
post:actors   | post:movies
patch:actors  | patch:movies
```

## Endpoints

GET '/actors'
- Fetches a dictionary of actors in which the keys are the ids and the value is the corresponding actor
- Request Arguments: token
- Returns: A dictionary of objects with single key and values 
```bash
{
    "actors": [
        {
            "First Name": "Michael",
            "Last Name": "George",
            "age": 66,
            "gender": "female",
            "id": 3
        },
        {
            "First Name": "Jason",
            "Last Name": "Johnson",
            "age": 55,
            "gender": "male",
            "id": 4
        }
    ],
    "success": true
}
```

GET '/movies'
- Fetches a dictionary of movies in which the keys are the ids and the value is the corresponding string of the movie
- Request Arguments: token
- Returns: A dictionary of objects with single key and values 
```bash
{
    "movies": [
        {
            "id": 6,
            "release-date": "25 Oct 1983",
            "title": "Rock House"
        },
    ],
    "success": true,
}
```

GET '/actors/<int:actor_id>'
- Fetches a specific actor
- Request Arguments: token, actor_id 
- Returns: The specific actor as object
```bash
{
    "First Name": "Jason",
    "Last Name": "Johnson",
    "age": 55,
    "gender": "male",
    "id": 7,
    "success": true
}
```

GET '/movies/<int:movie_id>'
- Fetches a specific movie
- Request Arguments: token, movie_id 
- Returns: The specific movie as object
```bash
{
    "id": 12,
    "release-date": "01 Oct 1990",
    "success": true,
    "title": "Blues Brothers"
}
```

DELETE '/actors/<int:actor_id>'
- Deletes a specific actor
- Request Arguments: token, actor_id 
- Returns: The ID of the deleted actor 
```bash
{
    "deleted": 5,
    "success": true
}
```

DELETE '/movies/<int:movie_id>'
- Deletes a specific movie
- Request Arguments: token, movie_id 
- Returns: The ID of the deleted movie 
```bash
{
    "deleted": 6,
    "success": true
}
```

POST '/actors'
- Adds an actor to the database 
- Request Arguments: token
- Returns: A success response and the name of the actor that was added
```bash
{
    "first-name": "Kristen",
    "last-name": "Jacobs",
    "success": true
}
```

POST '/movies'
- Adds a movie to the database 
- Request Arguments: token
- Returns: A success response and the 
```bash
{
    "release date": "06 Mar 1965",
    "success": true,
    "title": "Count Dracula"
}
```

PATCH '/movies/<int:actor_id>'
- Updates an actor in the database 
- Request Arguments: token, actor_id
- Returns: Success respoinse and the ID of the actor updated
```bash
{
    "Updated Actor ID": 6,
    "success": true
}
```

PATCH '/movies/<int:movie_id>'
- Updates a movie in the database 
- Request Arguments: token, movie_id
- Returns: Success respoinse and the ID of the movie updated
```bash
{
    "Updated Movie ID": 7,
    "success": true
}
```
