from flask import Flask, render_template, jsonify, request
from flaskext.mysql import MySQL

# General Settings
app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'assignment_3'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_PASSWORD'] = 'awolin82'

mysql = MySQL()
mysql.init_app(app)

# MySQL connector
conn = mysql.connect()

cursor = conn.cursor()

#Give context for tables
def get_table_context(cursor, cursor_data):
    ''' returns name of columns from query in data[0]
        takes a cursor and data from a fetchall()
    '''
    cursor_data = list(cursor_data)
    cursor_data.insert(0,tuple([i[0] for i in cursor.description]))
    data = tuple(cursor_data)
    return data

# Routes to index page
@app.route('/')
def main():

    cursor.execute("select * from book")

    data = cursor.fetchall()
    return render_template('index.html', data=data)

@app.route('/author')
def author():

    cursor.execute("select * from author")

    data = cursor.fetchall()
    return render_template('author.html', data=data)

@app.route('/copy')
def copy():

    cursor.execute("select * from copy")

    data = cursor.fetchall()
    return render_template('copy.html', data=data)

@app.route('/publisher')
def publisher():

    cursor.execute("select * from publisher")

    data = cursor.fetchall()
    return render_template('publisher.html', data=data)

@app.route('/search', methods=['GET', 'POST'])
def search():
    print(request.form['search'])
    if request.method == "POST":
        cursor.execute("{}".format(request.form['search']))
        cursor_data = cursor.fetchall()
        data = get_table_context(cursor, cursor_data)

    return render_template('search.html', data=data)

# This allows app to run with standar python commnand
if __name__ == "__main__":
    app.run()
