import resource
from flask import Flask, request, jsonify, render_template, url_for, redirect,flash
import sqlite3

app = Flask(__name__)
app.secret_key = "ksjowokspwjsjsd"

def connect_to_db():
    connect = None
    try:
        connect = sqlite3.connect("movies.db")
    except sqlite3.Error as e:
        print(e)
    return connect

@app.route('/')
def home():
    connection = connect_to_db()
    cursor = connection.execute("select * from movies")
    all_movie = cursor.fetchall()
    return render_template("index.html", movie_data = all_movie)

@app.route('/add-movie', methods=['POST'])
def add_movie():
    connection = connect_to_db()
    cursor = connection.cursor()

    if request.method == 'POST':
        new_movie_name = request.form['Movie_Name']
        new_release_date = request.form['Release_Date']
        new_watched_status = request.form['Watched_Status']

        cursor.execute("""insert into movies (Movie_Name, Release_Date, Watched_Status)
        values (?, ?, ?)""", (new_movie_name, new_release_date, new_watched_status))

        connection.commit()
        flash("New Movies Has Been Added Successfully")
        return redirect(url_for('home'))

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_movie(id):

    connection = connect_to_db()
    cursor = connection.cursor()

    if request.method == 'POST':
        query = """update movies
                    set Release_Date=?,
                        Movie_Name=?,
                        Watched_Status=?
                    where id=?"""

        Release_Date = request.form['Release_Date_Edit']
        Movie_Name = request.form['Movie_Name_Edit']
        Watched_Status = request.form['Watched_Status_Edit']
        
        cursor.execute(query, (Release_Date, Movie_Name, Watched_Status, id))
        connection.commit()
        
    return redirect(url_for('home'))

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete_movie(id):

    connection = connect_to_db()
    cursor = connection.cursor()

    query = """delete from movies where id=?"""
    cursor.execute(query, (id,))
    connection.commit()

    return redirect(url_for('home'))

@app.route('/all-movie', methods=['GET'])
def all_movies():
    connection = connect_to_db()
    cursor = connection.cursor()

    if request.method == 'GET':
        cursor = connection.execute("select * from movies")

        movie_dict = [ dict(id=row[0], Movie_Name=row[1], Release_Date=row[2], Watched_Status=row[3])
                        for row in cursor.fetchall()]
        return jsonify(movie_dict)

@app.route('/all-movie/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def single_movie(id):
    connection = connect_to_db()
    cursor = connection.cursor()

    if request.method == 'GET':
        cursor = connection.execute("select * from movies where id=?", (id,))
        movie = cursor.fetchall()
        return jsonify(movie)

    if request.method == 'PUT':
        query = """update movies
                    set Release_Date=?,
                        Movie_Name=?,
                        Watched_Status=?
                    where id=?"""

        Release_Date = request.form['Release_Date']
        Movie_Name = request.form['Movie_Name']
        Watched_Status = request.form['Watched_Status']
        
        update_movie = {
            'id': id,
            'Release_Date': Release_Date,
            'Movie_Name': Movie_Name,
            'Watched_Status': Watched_Status}
        
        cursor.execute(query, (Release_Date, Movie_Name, Watched_Status, id))
        connection.commit()
        return jsonify(update_movie)

    if request.method == 'DELETE':

        query = """delete from movies where id=?"""
        cursor.execute(query, (id,))
        connection.commit()

if __name__ == "__main__":
    app.run(debug=True)