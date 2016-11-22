from flask import Flask, render_template, jsonify
from flaskext.mysql import MySQL

# General Settings
app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'assignment_3'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql = MySQL()
mysql.init_app(app)

# MySQL connector
conn = mysql.connect()

cursor = conn.cursor()

# Routes to index page
@app.route('/')
def main():

    cursor.execute("select * from book")

    data = cursor.fetchall();
    return render_template('index.html', data=data)

@app.route('/author')
def author():

    cursor.execute("select * from author")

    data = cursor.fetchall();
    return render_template('author.html', data=data)

@app.route('/copy')
def copy():

    cursor.execute("select * from copy")

    data = cursor.fetchall();
    return render_template('copy.html', data=data)

@app.route('/publisher')
def publisher():

    cursor.execute("select * from publisher")

    data = cursor.fetchall();
    return render_template('publisher.html', data=data)

# This allows app to run with standar python commnand
if __name__ == "__main__":
    app.run()
