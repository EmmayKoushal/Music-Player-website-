from crypt import methods
from flask import Flask, render_template, request, session, redirect, url_for
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = "hello"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///App.db'
app.config['SQLAlchemy_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(minutes=5)

#ALL DATABASE CODE
db = SQLAlchemy(app)

class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(20), nullable=False, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class songs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    song_name = db.Column(db.String(100), nullable=False)
    uri = db.Column(db.String(100), nullable=False, unique=True)
    danceability = db.Column(db.Float, nullable=False)
    energy = db.Column(db.Float, nullable=False)
    key = db.Column(db.Integer, nullable=False)
    loudness = db.Column(db.Float, nullable=False)
    speechiness = db.Column(db.Float, nullable=False)
    acousticness = db.Column(db.Float, nullable=False)
    instrumentalness = db.Column(db.Float, nullable=False)
    liveness = db.Column(db.Float, nullable=False)
    valence = db.Column(db.Float, nullable=False)  
    tempo = db.Column(db.Float, nullable=False)
    artist_name = db.Column(db.String(100), nullable=False)
    album = db.Column(db.String(100), nullable=False)
    mood = db.Column(db.String(100), nullable=False)
    language = db.Column(db.String(100), nullable=False)
    category = db.Column(db.Float, nullable=False)
    dc0 = db.Column(db.Float, nullable=False)
    dc1 = db.Column(db.Float, nullable=False)
    dc2 = db.Column(db.Float, nullable=False)
    dc3 = db.Column(db.Float, nullable=False)


class recently_played(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    song_id = db.Column(db.Integer, nullable=False)
    song_mood = db.Column(db.String(100), nullable=False)
    song_languages = db.Column(db.String(100), nullable=False)
    song_artist = db.Column(db.String(100), nullable=False)
    frequency = db.Column(db.Integer, nullable=False)


# DATABASE CODE ENDS HERE

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods = ["POST", "GET"])
def login():
    if request.method == 'POST':
        session.permanent = True
        email = request.form['email']
        password = request.form['pass']

        if email != "" and password != "":
            user = users.query.filter_by(email=email).first()
            if user.check_password(request.form['pass']):
                name = user.name 
                session['name'] = name
                return redirect(url_for('Home'))
            else:
                return render_template('Login.html', msg="Invalid Password !")
        else:
            return render_template('Login.html', msg="Please fill all the details!")
    else:
        if 'name' in session:
            return redirect(url_for('Home'))
        return render_template('Login.html', msg="")

@app.route('/Home')
def Home():
    if 'name' in session:
        name = session['name']
        return render_template('home.html',name=name)
    else:
        return redirect(url_for('login'))

@app.route('/SignUp', methods = ['POST', 'GET'])
def signup():
    if request.method == 'POST':
        form = request.form
        count = users.query.filter_by(email=form['email']).count()
        if count == 0:  
            if form['name'] == "" or form['email'] == "" or form['pass'] == "":
                return render_template('SignUp.html', msg = "Please Fill All Details !")
            else:              
                user = users(
                    name = form['name'],
                    email = form['email']
                )
                user.set_password(form['pass'])
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))
        else:
            return render_template('SignUp.html', msg = "Email Already Exists !")
    else:
        return render_template('SignUp.html', msg="")

@app.route('/logout')
def logout():
    session.pop('name', None)
    return redirect(url_for('login'))

@app.route('/music',methods = ['GET', 'POST'])
def music():
    if request.method == 'POST':
        link = request.form['data']
        print(link)
    return render_template('music.html', recents = ["song1", "song2", "song3"])


if __name__ == '__main__':
    app.run(debug=True)