from flask import Flask, render_template, request, redirect
from neo4j import GraphDatabase
import os

app = Flask(__name__)

URI = os.getenv("NEO4J_URI")
USER = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")

driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

@app.route("/")
def index():
    with driver.session() as session:
        result = session.run("MATCH (m:Movie) RETURN m")
        movies = [record["m"] for record in result]
    return render_template("index.html", movies=movies)

@app.route("/add", methods=["POST"])
def add_movie():
    title = request.form["title"]
    year = int(request.form["year"])
    genre = request.form["genre"]

    with driver.session() as session:
        session.run(
            "CREATE (m:Movie {title:$title, year:$year, genre:$genre})",
            title=title, year=year, genre=genre
        )
    return redirect("/")

@app.route("/filter")
def filter_movie():
    genre = request.args.get("genre")
    with driver.session() as session:
        result = session.run(
            "MATCH (m:Movie {genre:$genre}) RETURN m",
            genre=genre
        )
        movies = [record["m"] for record in result]
    return render_template("index.html", movies=movies)

if __name__ == "__main__":
    app.run()
