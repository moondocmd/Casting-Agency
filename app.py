import os
import dateutil.parser
import babel
import json
import time
from time import gmtime, strftime
from datetime import date, datetime
from flask import Flask, request, abort, jsonify, render_template, session, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db_drop_and_create_all, setup_db, Actor, Movie
from auth.auth import AuthError, requires_auth
from authlib.integrations.flask_client import OAuth


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)
    # db_drop_and_create_all()
    return app


app = create_app()
app.secret_key = os.urandom(24)
oauth = OAuth(app)

auth0 = oauth.register(
    'auth0',
    client_id='sTJG5iVLA8tx8loet75JrKYpTBmWTetY',
    client_secret='lsWRwh0KUhyqx06hKNf8OWPs_qXVQpz7lL7Vvou9-D5L9R1IscpvEyehq3iOce6p',
    api_base_url='https://full-stack-2020.us.auth0.com',
    access_token_url='https://full-stack-2020.us.auth0.com/oauth/token',
    authorize_url='https://full-stack-2020.us.auth0.com/authorize',
    client_kwargs={
        'scope': 'openid profile email',
    },
)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)


def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)


# ROUTES
# route handler for home page
@app.route('/')
def index():
    return render_template('templates/home.html')


@app.route('/login')
def login():
    return auth0.authorize_redirect(redirect_uri='http://localhost:5000/callback')


@app.route('/callback')
def callback_handling():
    # Handles response from token endpoint
    auth0.authorize_access_token()
    resp = auth0.get('userinfo')
    userinfo = resp.json()

    # Store the user information in flask session.
    session['jwt_payload'] = userinfo
    session['profile'] = {
        'user_id': userinfo['sub'],
        'name': userinfo['name'],
        'picture': userinfo['picture']
    }
    return redirect('/dashboard')


@app.route('/dashboard')
def dashboard():
    return render_template(
        'dashboard.html',
        userinfo=session['profile'],
        userinfo_pretty=json.dumps(session['jwt_payload'], indent=4)
        )


@app.route("/authorization/url", methods=["GET"])
def generate_auth_url():
    url = f'https://full-stack-2020.us.auth0.com/authorize' \
        f'?audience=casting' \
        f'&response_type=token&client_id=' \
        f'sTJG5iVLA8tx8loet75JrKYpTBmWTetY&redirect_uri=' \
        f'http://localhost:5000/callback'
    return jsonify({
        'url': url
    })


@app.route('/actors', methods=['GET'])
@requires_auth('get:actors')
def get_actors(token):
    try:
        actors = []
        for actor in Actor.query.order_by(Actor.id).all():
            actors.append({
                "id": actor.id,
                "First Name": actor.fname,
                "Last Name": actor.lname,
                "age": actor.age,
                "gender": actor.gender
            })
        return jsonify({
            "success": True,
            "actors": actors
        }), 200
    except Exception:
        abort(404)


@app.route('/movies', methods=['GET'])
@requires_auth('get:movies')
def get_movies(token):
    try:
        movies = []
        for movie in Movie.query.order_by(Movie.id).all():
            movies.append({
                "id": movie.id,
                "title": movie.title,
                "release-date": movie.release,
            })
        return jsonify({
            "success": True,
            "movies": movies
        }), 200
    except Exception:
        abort(404)


@app.route('/actors/<int:actor_id>', methods=['GET'])
@requires_auth('get:actors')
def get_actor(token, actor_id):
    try:
        actor = Actor.query.get(actor_id)
        if actor is None:
            abort(404)
        return jsonify({
            "success": True,
            "id": actor.id,
            "First Name": actor.fname,
            "Last Name": actor.lname,
            "age": actor.age,
            "gender": actor.gender
        }), 200
    except Exception:
        abort(404)


@app.route('/movies/<int:movie_id>', methods=['GET'])
@requires_auth('get:movies')
def get_movie(token, movie_id):
    try:
        movie = Movie.query.get(movie_id)
        if movie is None:
            abort(404)
        return jsonify({
            "success": True,
            "id": movie.id,
            "title": movie.title,
            "release-date": movie.release
        }), 200
    except Exception:
        abort(404)


@app.route('/actors', methods=['POST'])
@requires_auth('post:actors')
def new_actor(token):
    try:
        body = request.get_json()
        fname = body.get('fname', None)
        lname = body.get('lname', None)
        age = body.get('age', None)
        gender = body.get('gender', None)
        new_actor = Actor(fname=fname, lname=lname, age=age, gender=gender)
        new_actor.insert()
        return jsonify({
            'success': True,
            'first-name': fname,
            'last-name': lname
        }), 200
    except Exception:
        abort(422)


@app.route('/movies', methods=['POST'])
@requires_auth('post:movies')
def new_movie(token):
    try:
        body = request.get_json()
        title = body.get('title', None)
        release = time.strptime(body.get('release'), "%m/%d/%Y")
        new_movie = Movie(title=title, release=strftime("%d %b %Y", release))
        new_movie.insert()
        return jsonify({
            'success': True,
            'title': title,
            'release date': strftime("%d %b %Y", release)
        }), 200
    except Exception:
        abort(422)


@app.route('/movies/<int:movie_id>', methods=['PATCH'])
@requires_auth('patch:movies')
def update_movie(token, movie_id):
    try:
        movie = Movie.query.filter_by(id=movie_id).one_or_none()

        if(movie is None):
            abort(404)

        body = request.get_json()
        movie.title = body.get('title', movie.title)
        if('release' in body):
            release = time.strptime(body.get('release'), "%m/%d/%Y")
            movie.release = strftime("%d %b %Y", release)

        movie.update()

        return jsonify({
            'success': True,
            'Updated Movie ID': movie.id
        }), 200

    except Exception:
        abort(422)


@app.route('/actors/<int:actor_id>', methods=['PATCH'])
@requires_auth('patch:actors')
def update_actor(token, actor_id):
    try:
        actor = Actor.query.filter_by(id=actor_id).one_or_none()
        if(actor is None):
            abort(404)

        body = request.get_json()
        actor.fname = body.get('fname', actor.fname)
        actor.lname = body.get('lname', actor.lname)
        actor.age = body.get('age', actor.age)
        actor.gender = body.get('gender', actor.gender)
        actor.update()

        return jsonify({
            'success': True,
            'Updated Actor ID': actor.id
        }), 200
    except Exception:
        abort(422)


@app.route('/actors/<int:actor_id>', methods=['DELETE'])
@requires_auth('delete:actors')
def delete_actor(token, actor_id):
    try:
        actor = Actor.query.get(actor_id)
        actor.delete()
        return jsonify({
            'success': True,
            'deleted': actor.id
        }), 200
    except Exception:
        abort(422)


@app.route('/movies/<int:movie_id>', methods=['DELETE'])
@requires_auth('delete:movies')
def delete_movie(token, movie_id):
    try:
        movie = Movie.query.get(movie_id)
        movie.delete()
        return jsonify({
            'success': True,
            'deleted': movie.id
        }), 200
    except Exception:
        abort(422)


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(404)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Resource not found"
    }), 404


@app.errorhandler(401)
def bad_request(error):
    return jsonify({
      "success": False,
      "error": 401,
      "message": "Authorization header is expected"
      }), 401


@app.errorhandler(AuthError)
def auth_error(ex):
    return jsonify({
        "success": False,
        "error": ex.status_code,
        "message": ex.error['description']
    }), ex.status_code
