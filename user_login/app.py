from flask import Flask, render_template, redirect, request, session

app = Flask(__name__)
app.secret_key = "secret key"

@app.route('/')
def home():
    return redirect('/login')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['pass'] == 'admin':
            session['user'] = request.form['username']
            return redirect('http://13.229.208.238:8050/')
    error = 'Invalid Credentials'
    return render_template('index.html', error=error)

if __name__ == '__main__':
    app.run(port=1234)