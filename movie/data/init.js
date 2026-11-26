db = db.getSiblingDB("moviedb");

const fs = require("fs");

const moviesData = JSON.parse(fs.readFileSync("/seed/movies.json", "utf8"));
db.movies.drop();
db.movies.insertMany(moviesData.movies);

const actorsData = JSON.parse(fs.readFileSync("/seed/actors.json", "utf8"));
db.actors.drop();
db.actors.insertMany(actorsData.actors);
