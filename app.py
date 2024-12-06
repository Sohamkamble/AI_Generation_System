from flask import Flask, render_template, request, redirect, url_for, session
from models import db, User, Content
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'secret_key_12345'

db.init_app(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)

# Routes for Registration and Login
@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        username = request.form.get('username')
        email = request.form.get('email')
        password = bcrypt.generate_password_hash(request.form.get('password')).decode('utf-8')

        user = User(user_id = user_id, username = username, email = email, password = password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        password = request.form.get('password')
        user = User.query.filter_by(user_id = user_id).first()
        if user and bcrypt.check_password_hash(user.password, password):
            session['user_id'] = user_id
            return redirect(url_for('index'))
        else:
            return "Invalid login details"
    return render_template('login.html')

# Routes for Text Prompt Submission
@ app.route('/', methods = ['GET', 'POST'])
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        prompt = request.form.get('prompt')
        user = User.query.filter+by(user_id = session['user_id']).first()
        content = Content(user_id = user.id, prompt = prompt)
        db.session.commit()
        return redirect(url_for('gallery'))
    
    return render_template('index.html')

@app.route('/gallery')
def gallery():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.filter_by(user_id = session['user_id']).first()
    content = Content.query.filter_by(user_id = user.user_id).first()

    if content.status == 'Processing':
        return "Your content is being generated. Please check back later."
    
    video_paths = content.video_paths.split(',') if content.video_paths else []
    image_paths = content.image_paths.split(',') if content.image_paths else []

    return render_template('gallery.html', videos = video_paths, images = image_paths)
    
if __name__ == '__main__':
    app.run(debug=True)