# app.py
import json

import utils
from models import request, app, db
from flask_restx import Api, Resource
from schemas import movie_schema, movies_schema, directors_schema, director_schema, genre_schema, genres_schema
from models import Movie, Director, Genre


api = Api(app)

movies_ns = api.namespace("movies")
director_ns = api.namespace("directors")
genre_ns = api.namespace("genres")


# Movies routs
@movies_ns.route("/")
class MoviesView(Resource):

    def get(self):
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('page_size', 10))
        did = request.args.get('director_id', None)
        gid = request.args.get('genre_id', None)
        movies_query = db.session.query(Movie.title, Movie.description, Movie.year, Movie.rating, Movie.trailer,
                     Genre.name.label('genre'), Director.name.label('director')).join(Genre).join(Director)
        if did:
            movies_query = movies_query.filter(Movie.director_id == did)
        if gid:
            movies_query = movies_query.filter(Movie.genre_id == did)

        movies_query = utils.pagination(movies_query, page, page_size)
        return movies_schema.dump(movies_query), 200

    def post(self):
        movie_data = request.json
        movie_data = Movie(**movie_data)
        db.session.add(movie_data)
        db.session.commit()
        return "The Movielist updated", 201


@movies_ns.route("/<int:mid>")
class MoviesView(Resource):

    def get(self, mid):
        movie = db.session.query(Movie.title, Movie.description, Movie.year, Movie.rating, Movie.trailer,
                                      Genre.name.label('genre'), Director.name.label('director')).join(Genre).join(Director).filter(Movie.id == mid).one()
        return movie_schema.dump(movie), 200

    def put(self, mid):
        movie = db.session.query(Movie).filter(Movie.id == mid).one()
        movie_put_json = request.json
        movie.title = movie_put_json['title']
        movie.year = movie_put_json['year']
        movie.description = movie_put_json['description']
        movie.trailer = movie_put_json['trailer']
        movie.rating = movie_put_json['rating']
        movie.genre_id = movie_put_json['genre_id']
        movie.director_id = movie_put_json['director_id']
        db.session.add(movie)
        db.session.commit()
        return "The movie has been changed", 202

    def delete(self, mid):
        db.session.query(Movie).filter(Movie.id == mid).delete()
        db.session.commit()
        return "The movie has been deleted", 203


# Directors routs
@director_ns.route("/")
class DirectorView(Resource):

    def get(self):
        directors = db.session.query(Director).all()
        return directors_schema.dump(directors), 201

    def post(self):
        directors_data = request.json
        directors_data = Director(**directors_data)
        db.session.add(directors_data)
        db.session.commit()
        return "The list of directors updated", 201


@director_ns.route("/<int:did>")
class DirectorView(Resource):

    def get(self, did):
        director = db.session.query(Director).filter(Director.id == did).one()
        return director_schema.dump(director), 201

    def put(self, did):
        director = db.session.query(Director).filter(Director.id == did).one()
        director_put_json = request.json
        director.name = director_put_json['name']
        db.session.add(director)
        db.session.commit()
        return "The movie has been changed", 202

    def delete(self, did):
        db.session.query(Director).filter(Director.id == did).delete()
        db.session.commit()
        return "The movie has been deleted", 203


# Genres routs
@genre_ns.route("/")
class GenreView(Resource):

    def get(self):
        genres = db.session.query(Genre).all()
        return genres_schema.dump(genres), 201

    def post(self):
        genre_data = request.json
        genre_data = Genre(**genre_data)
        db.session.add(genre_data)
        db.session.commit()
        return "The lust of genres updated", 201


@genre_ns.route("/<int:gid>")
class GenreView(Resource):

    def get(self, gid):
        genre = db.session.query(Genre).filter(Genre.id == gid).one()
        return genre_schema.dump(genre), 201

    def put(self, gid):
        genre = db.session.query(Genre).filter(Genre.id == gid).one()
        genre_put_json = request.json
        genre.name = genre_put_json['name']
        db.session.add(genre)
        db.session.commit()
        return "The genre has been changed", 202

    def delete(self, gid):
        db.session.query(Genre).filter(Genre.id == gid).delete()
        db.session.commit()
        return "The genre has been deleted", 203


if __name__ == '__main__':
    app.run(debug=True)
