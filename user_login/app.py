import binascii
import hashlib
import os

from flask import Flask, render_template, redirect, request, session
import dbcon as db

app = Flask(__name__)
app.secret_key = "secret key"

@app.route('/')
def home():
    return redirect('/login')

@app.route('/login', methods=['GET','POST'])
def login():
    error = None
    colour = None
    if request.method == 'POST':
        if request.form['username'] != None and request.form['pass'] != None:
            username = request.form['username']
            password = request.form['pass']
            user = getUsers(username)
            print(user)
            if user != None and verify_password(user[1],password):
                session['user'] = request.form['username']
                return redirect('http://13.229.208.238:8050/')
        error = 'Invalid Credentials'
        colour = 'red'
    return render_template('index.html', error=error, colour=colour)

@app.route('/sign-up', methods=['GET','POST'])
def signup():
    error = None
    colour = None
    if request.method == 'POST':
        if request.form['username'] != None and request.form['pass'] != None:
            username = request.form['username']
            user = getUsers(username)
            if user is None:
                password = hash_password(request.form['pass'])
                setUsers(username,password)
                colour = 'green'
                return render_template('signup.html', error='Account Created!!', colour=colour)
            else:
                error = 'User Already Exsists!!'
                colour = 'red'
        else:
            error = 'Invalid Inputs'
            colour = 'red'
    return render_template('signup.html', error=error, colour=colour)

def getUsers(username):
    client = db.get_mysql_connection()
    select_query = 'select * from users where userID = \'%s\''
    # alter_query = 'alter table ticker_to_pin_id add column updated_date timestamp default NULL'
    # update_query = 'update ticker_to_pin_id set url_status = 1 where ticker = \"AAPL\"'
    cursor = client.cursor()
    select_query = select_query%(username)
    cursor.execute(select_query)
    users = cursor.fetchall()
    for user in users:
        return user
    # client2.commit()
    client.close
    return None

def setUsers(username, password):
    client = db.get_mysql_connection()
    query = 'insert into users values (\'%s\', \'%s\')'
    query = query%(username,password)
    cursor = client.cursor()
    cursor.execute(query)
    client.commit()
    client.close()

def hash_password(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                  salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')


def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user"""
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512',
                                  provided_password.encode('utf-8'),
                                  salt.encode('ascii'),
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    print(pwdhash == stored_password)
    return pwdhash == stored_password

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

