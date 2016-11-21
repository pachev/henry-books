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


# Routes to index page
@app.route('/')
def main():
    return render_template('index.html')

@app.route('/data')
def showData():
    # MySQL connector
    conn = mysql.connect()

    cursor = conn.cursor()

    cursor.execute("select * from book")

    data = cursor.fetchall();
    return jsonify(data)

# This allows app to run with standar python commnand
if __name__ == "__main__":
    app.run()
