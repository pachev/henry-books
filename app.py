from flask import Flask, render_template, jsonify, request, redirect, url_for
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

def form_clean(form_input, action):
    c = form_input.split()
    if c[0] == action.upper():
        return True
    return False
# Routes to index page
@app.route('/book', methods=['GET', 'POST'])
def main():

    cursor.execute("select * from book")

    cursor_data = cursor.fetchall()
    data = get_table_context(cursor, cursor_data)


    return render_template('index.html', data=data)

@app.route('/author')
def author():

    cursor.execute("select * from author")

    cursor_data = cursor.fetchall()
    data = get_table_context(cursor, cursor_data)

    return render_template('index.html', data=data)

@app.route('/copy')
def copy():


    cursor.execute("select * from copy")

    cursor_data = cursor.fetchall()
    data = get_table_context(cursor, cursor_data)

    return render_template('index.html', data=data)

@app.route('/publisher')
def publisher():

    cursor.execute("select * from publisher")

    cursor_data = cursor.fetchall()
    data = get_table_context(cursor, cursor_data)

    return render_template('index.html', data=data)

@app.route('/search', methods=['GET', 'POST'])
def index():
    query = "SELECT b.title, c.quality, c.price, br.branchname, a.authorfirst,\
            a.authorlast, p.publishername \
            FROM \
            BOOK b LEFT JOIN \
            (COPY c, BRANCH br, PUBLISHER p, WROTE w, AUTHOR a) \
            ON \
            (c.bookcode=b.bookcode AND \
            c.branchnum=br.branchnum AND \
            b.bookcode=w.bookcode) \
            WHERE \
            b.title LIKE \"%{}%\" AND \
            p.publishercode=b.publishercode AND \
            a.authornum=w.authornum"

    if request.method == "GET":
        form_input = query.format(request.args.get('search').upper())
        cursor.execute("{}".format(form_input))
        cursor_data = cursor.fetchall()
        data = get_table_context(cursor, cursor_data)

    return render_template('index.html', data=data)

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

@app.route('/delete-book', methods=['POST'])
def delete_book():
    cursor.execute("delete from book where bookcode = \'{}\'".format(request.form.get("book_to_delete")))
    return redirect(url_for('main'))

@app.route('/delete-author', methods=['POST'])
def delete_author():
    cursor.execute("delete from author where authornum = \'{}\'".format(request.form.get("author_to_delete")))
    return redirect(url_for('author'))

@app.route('/delete-publisher', methods=['POST'])
def delete_publisher():
    cursor.execute("delete from publisher where publishercode = \'{}\'".format(request.form.get("publisher_to_delete")))
    return redirect(url_for('publisher'))

@app.route('/delete-copy', methods=['POST'])
def delete_copy():
    cursor.execute("delete from copy where bookcode = \'{}\'".format(request.form.get("copy_to_delete")))
    return redirect(url_for('copy'))

# This allows app to run with standar python commnand
if __name__ == "__main__":
    app.run()
