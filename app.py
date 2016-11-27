from flask import Flask,flash, render_template, request, redirect, session, current_app, url_for

from flaskext.mysql import MySQL

# General Settings
app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'user'
app.config['MYSQL_DATABASE_PASSWORD'] = 'pw'
app.config['MYSQL_DATABASE_DB'] = 'henry'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

# Uncomment the line below to use the remote database as oppose to a henry one on localhost
# app.config['MYSQL_DATABASE_HOST'] = '107.170.108.43'

app.config['SECRET_KEY'] = 'A-UUID-123-GOES-4567-HERE'

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
@app.route('/')
def main():
    return render_template('index.html')

@app.route('/book', methods=['GET', 'POST'])
def book():

    cursor.execute("select * from Book")

    cursor_data = cursor.fetchall()
    data = get_table_context(cursor, cursor_data)

    return render_template('list-view.html', data=data, editpath='book')

@app.route('/author')
def author():

    cursor.execute("select * from Author")

    cursor_data = cursor.fetchall()
    data = get_table_context(cursor, cursor_data)

    return render_template('list-view.html', data=data, editpath='author')

@app.route('/copy')
def copy():

    cursor.execute("select * from Copy")

    cursor_data = cursor.fetchall()
    data = get_table_context(cursor, cursor_data)

    return render_template('list-view.html', data=data, editpath='copy')

@app.route('/publisher')
def publisher():

    cursor.execute("select * from Publisher")

    cursor_data = cursor.fetchall()
    data = get_table_context(cursor, cursor_data)

    return render_template('list-view.html', data=data, editpath='publisher')

@app.route('/search', methods=['GET', 'POST'])
def index():
    query = "SELECT b.title, c.quality, c.price, br.branchName, a.authorFirst,\
            a.authorLast, p.publisherName \
            FROM \
            Book b LEFT JOIN \
            (COPY c, Branch br, Publisher p, Wrote w, Author a) \
            ON \
            (c.bookCode=b.bookCode AND \
            c.branchNum=br.branchNum AND \
            b.bookCode=w.bookCode) \
            WHERE \
            b.title LIKE \"%{}%\" AND \
            p.publisherCode=b.publisherCode AND \
            a.authorNum=w.authorNum"

    if request.method == "GET":
        form_input = query.format(request.args.get('search').upper())
        cursor.execute("{}".format(form_input))
        cursor_data = cursor.fetchall()
        data = get_table_context(cursor, cursor_data)

    return render_template('list-view.html', data=data)

@app.route('/editbook', methods=['POST'])
def editBook():
    _title = request.form['edittitle']
    _bookcode = request.form['editbookCode']
    _publishercode = request.form['editpublisherCode']
    _type = request.form['edittype']
    _paperback = request.form['editpaperback']

    query = "UPDATE Book SET bookCode=\"{}\", title=\"{}\", publisherCode=\"{}\",\
            type=\"{}\", paperback=\"{}\" WHERE\
            bookcode=\"{}\""
    update = query.format(_bookcode, _title, _publishercode, _type, _paperback, _bookcode)

    try:
        cursor.execute("{}".format(update))
        data = cursor.fetchall()
        if len(data) is 0:
            flash('Row sucessfully updated', 'success')
            return redirect('/book')
        else:
            flash('Something went terribly wrong', 'error')
            return redirect('/book')
    except Exception as e:
        flash('Something went terribly wrong', 'error')
        return redirect('/')

@app.route('/editauthor', methods=['POST'])
def editAuthor():

    author_num = request.form['editauthorNum']
    author_last = request.form['editauthorLast']
    author_first = request.form['editauthorFirst']

    print(request.form)

    query = "UPDATE Author SET authorLast=\"{}\", authorFirst=\"{}\"  WHERE authorNum={}"

    update = query.format(author_last,author_last, author_num)

    print(update)

    try:
        cursor.execute("{}".format(update))
        data = cursor.fetchall()
        if len(data) is 0:
            flash('Row sucessfully updated', 'success')
            return redirect('/author')
        else:
            flash('Something went terribly wrong', 'error')
            return redirect('/author')
    except Exception as e:
        flash('Something went terribly wrong', 'error')
        return redirect('/')

@app.route('/editpublisher', methods=['POST'])
def editPublisher():

    print(request.form)
    _publishercode = request.form['editpublisherCode']
    _publishername = request.form['editpublisherName']
    _city = request.form['editcity']


    query = "UPDATE Publisher  SET publisherName=\"{}\", city=\"{}\"  WHERE publisherCode=\"{}\""

    update = query.format(_publishername, _city, _publishercode)

    print(update)

    try:
        cursor.execute("{}".format(update))
        data = cursor.fetchall()
        if len(data) is 0:
            flash('Row sucessfully updated', 'success')
            return redirect('/publisher')
        else:
            flash('Something went terribly wrong', 'error')
            return redirect('/publisher')
    except Exception as e:
        flash('Something went terribly wrong', 'error')
        return redirect('/')

@app.route('/editcopy', methods=['POST'])
def editCopy():
    _bookcode = request.form['editbookCode']
    _branchnum = request.form['editbranchNum']
    _copynum = request.form['editcopyNum']
    _quality = request.form['editquality']
    _price = request.form['editprice']

    print(request.form)
    query = "UPDATE Copy SET bookCode=\"{}\", branchNum={}, copyNum={},\
            quality=\"{}\", price={} WHERE\
            bookCode=\"{}\" AND copyNum={}"
    update = query.format(_bookcode, _branchnum, _copynum, _quality, _price, _bookcode, _copynum)

    print(update)

    try:
        cursor.execute("{}".format(update))
        data = cursor.fetchall()
        if len(data) is 0:
            flash('Row sucessfully updated', 'success')
            return redirect('/copy')
        else:
            flash('Something went terribly wrong', 'error')
            return redirect('/copy')
    except Exception as e:
        flash('Something went terribly wrong', 'error')
        return redirect('/')



# DELETE OPERATIONS
@app.route('/delete-book', methods=['POST'])
def delete_book():
    '''Function View For Deleting Books'''

    cursor.execute("delete from Book where bookCode = \'{}\'".format(request.form.get("book_to_delete")))
    return redirect(url_for('book'))

@app.route('/delete-author', methods=['POST'])
def delete_author():
    '''Function View For Deleting Authors'''
    cursor.execute("delete from Author where authorNum = \'{}\'".format(request.form.get("author_to_delete")))
    return redirect(url_for('author'))

@app.route('/delete-publisher', methods=['POST'])
def delete_publisher():
    '''Function View For Deleting Publishers'''
    cursor.execute("delete from Publisher where publisherCode = \'{}\'".format(request.form.get("publisher_to_delete")))
    return redirect(url_for('publisher'))

@app.route('/delete-copy', methods=['POST'])
def delete_copy():
    '''Function View For Deleting Copies'''
    cursor.execute("delete from Copy where bookCode = \'{}\'".format(request.form.get("copy_to_delete")))
    return redirect(url_for('copy'))

# ADD OPERATIONS

@app.route('/add-book', methods=['POST'])
def add_book():
    '''Function View For Adding Books'''

    _title = request.form['addtitle']
    _bookcode = request.form['addbookCode']
    _publishercode = request.form['addpublisherCode']
    _type = request.form['addtype']
    _paperback = request.form['addpaperback']

    print(request.form)
    query = ("INSERT INTO Book "
            "(bookCode, title, publisherCode, type, paperback)"
            "VALUES (\"{}\", \"{}\", \"{}\", \"{}\", \"{}\")")
    add = query.format(_bookcode, _title, _publishercode, _type, _paperback)

    print(add)

    try:
        cursor.execute("{}".format(add))
        data = cursor.fetchall()
        if len(data) is 0:
            flash('Row sucessfully added', 'success')
            return redirect('/book')
        else:
            flash('Something went terribly wrong', 'error')
            return redirect('/book')
    except Exception as e:
        flash('Something went terribly wrong', 'error')
        return redirect('/')

@app.route('/add-author', methods=['POST'])
def add_author():
    '''Function View For Adding Authors'''

    _author_num = request.form['addauthorNum']
    _author_last = request.form['addauthorLast']
    _author_first = request.form['addauthorFirst']

    print(request.form)
    query = ("INSERT INTO Author "
            "(authorNum, authorLast, authorFirst)"
            " VALUES ({},\"{}\", \"{}\")")
    add = query.format(_author_num, _author_last, _author_first)

    print(add)

    try:
        cursor.execute("{}".format(add))
        data = cursor.fetchall()
        if len(data) is 0:
            flash('Row sucessfully added', 'success')
            return redirect('/author')
        else:
            flash('Something went terribly wrong', 'error')
            return redirect('/author')
    except Exception as e:
        flash('Something went terribly wrong', 'error')
        return redirect('/')

@app.route('/add-publisher', methods=['POST'])
def add_publisher():
    '''Function View For Adding Copies'''

    _publishercode = request.form['addpublisherCode']
    _publishername = request.form['addpublisherName']
    _city = request.form['addcity']

    print(request.form)
    query = ("INSERT INTO Publisher "
            "(publisherCode, publisherName, city)"
            "VALUES (\"{}\", \"{}\", \"{}\")")
    add = query.format(_publishercode, _publishername, _city)

    print(add)

    try:
        cursor.execute("{}".format(add))
        data = cursor.fetchall()
        if len(data) is 0:
            flash('Row sucessfully added', 'success')
            return redirect('/publisher')
        else:
            flash('Something went terribly wrong', 'error')
            return redirect('/publisher')
    except Exception as e:
        flash('Something went terribly wrong', 'error')
        return redirect('/')

@app.route('/add-copy', methods=['POST'])
def add_copy():
    '''Function View For Adding Copies'''

    _bookcode = request.form['addbookCode']
    _branchnum = request.form['addbranchNum']
    _copynum = request.form['addcopyNum']
    _quality = request.form['addquality']
    _price = request.form['addprice']

    print(request.form)
    query = ("INSERT INTO Copy"
            "(bookCode, branchNum, copyNum, quality, price)"
            "VALUES (\"{}\", {}, {}, \"{}\", {})")
    add = query.format(_bookcode, _branchnum, _copynum, _quality, _price, _bookcode, _copynum)

    print(add)

    try:
        cursor.execute("{}".format(add))
        data = cursor.fetchall()
        if len(data) is 0:
            flash('Row sucessfully added', 'success')
            return redirect('/copy')
        else:
            flash('Something went terribly wrong', 'error')
            return redirect('/copy')
    except Exception as e:
        flash('Something went terribly wrong', 'error')
        return redirect('/')

# This allows app to run with standar python commnand
if __name__ == "__main__":
    app.run()
