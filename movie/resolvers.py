import json
from uuid import uuid4


def movies(_,info):
    with open('{}/data/movies.json'.format("."), "r") as file:
        movies = json.load(file)
        return movies['movies']


def movie_with_id(_,info,_id):
    with open('{}/data/movies.json'.format("."), "r") as file:
        movies = json.load(file)
        for movie in movies['movies']:
            if movie['id'] == _id:
                return movie

            
def movie_with_title(_,info,_title):
    with open('{}/data/movies.json'.format("."), "r") as file:
        movies = json.load(file)
        return [movie for movie in movies['movies'] if _title in movie['title']]



def add_movie(_,info,_title,_director,_rating):
    newmovies = {}
    newmovie = {
        "id": str(uuid4()),
        "title": _title,
        "director": _director,
        "rating": _rating
    }
    with open('{}/data/movies.json'.format("."), "r") as rfile:
        movies = json.load(rfile)
        movies['movies'].append(newmovie)
        newmovies = movies
    with open('{}/data/movies.json'.format("."), "w") as wfile:
        json.dump(newmovies, wfile)
    return newmovie


def update_movie_rate(_,info,_id,_rate):
    newmovies = {}
    newmovie = {}
    with open('{}/data/movies.json'.format("."), "r") as rfile:
        movies = json.load(rfile)
        for movie in movies['movies']:
            if movie['id'] == _id:
                movie['rating'] = _rate
                newmovie = movie
                newmovies = movies
    with open('{}/data/movies.json'.format("."), "w") as wfile:
        json.dump(newmovies, wfile)
    return newmovie


def update_movie_title(_,info,_id,_title):
    newmovies = {}
    newmovie = {}
    with open('{}/data/movies.json'.format("."), "r") as rfile:
        movies = json.load(rfile)
        for movie in movies['movies']:
            if movie['id'] == _id:
                movie['title'] = _title
                newmovie = movie
                newmovies = movies
    with open('{}/data/movies.json'.format("."), "w") as wfile:
        json.dump(newmovies, wfile)
    return newmovie


def update_movie_director(_,info,_id,_director):
    newmovies = {}
    newmovie = {}
    with open('{}/data/movies.json'.format("."), "r") as rfile:
        movies = json.load(rfile)
        for movie in movies['movies']:
            if movie['id'] == _id:
                movie['director'] = _director
                newmovie = movie
                newmovies = movies
    with open('{}/data/movies.json'.format("."), "w") as wfile:
        json.dump(newmovies, wfile)
    return newmovie


def resolve_actors_in_movie(movie, info):
    with open('{}/data/actors.json'.format("."), "r") as file:
        actors = json.load(file)
        result = [actor for actor in actors['actors'] if movie['id'] in actor['films']]
        return result


def delete_movie(_, info, _id):
    remaining_movies = []
    try:
        with open("./data/movies.json", "r") as rfile:
            movies = json.load(rfile)

        original_movies = movies["movies"]
        for movie in original_movies:
            if movie["id"] != _id:
                remaining_movies += [movie]

        if len(remaining_movies) == len(original_movies):
            return {
                "success": False, 
                "message": "Movie not found"
            }

        movies["movies"] = remaining_movies
        with open("./data/movies.json", "w") as wfile:
            json.dump(movies, wfile)
    except Exception as error:
        return {
            "success": False, 
            "message": "Error deleting movie: {}".format(error)
        }
    
    return {
        "success": True, 
        "message": "Movie deleted successfully"
    }