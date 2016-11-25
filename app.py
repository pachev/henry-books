from flask import Flask, render_template, jsonify, request
from flaskext.mysql import MySQL

# General Settings
app = Flask(__name__, static_url_path='/static')

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
@app.route('/', methods=['GET', 'POST'])
def main():

    cursor.execute("select * from book")
    data = cursor.fetchall();

    # # Read the posted values
    # _title = request.form['title']
    # _bookcode = request.form['bookCode']
    # _publisherCode = request.form['publisherCode']
    # _type = request.form['type']
    # _paperback = request.form['paperback']
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

@app.route('/editbook', methods=['POST'])
def editBook():
    _title = request.form['editTitle']
    _bookcode = request.form['editBookcode']
    _publishercode = request.form['editPublishercode']
    _type = request.form['editType']
    _paperback = request.form['editPaperback']

    cursor.execute("""
        UPDATE book SET bookcode=%s, title=%s, publishercode=%s, 
        type=%s, paperback=%s WHERE bookcode=%s
    """,(_bookcode, _title, _publishercode, _type, _paperback, _bookcode))
    
    conn.commit()

    return(_title)

# This allows app to run with standar python commnand
if __name__ == "__main__":
    app.run()
