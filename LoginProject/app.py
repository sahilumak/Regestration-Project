from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = "your_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///demo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


@app.route('/')
def front():
    return render_template('front.html')

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):

        return f'<User {self.username}>'


with app.app_context():
    db.create_all()


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['user_id'] = user.id
            flash("Login Successful", "success")
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html',err='Invalid Details')
        
    return render_template('login.html')





@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return render_template('signup.html',err="Username already taken. Please choose another.")
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
           return render_template('signup.html',err="Email already taken. Please choose another.")

        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/login')
    else:
        return render_template('signup.html')
    
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user_id' not in session:
        flash("Please log in first", "warning")
        return redirect(url_for('login'))
    
    return render_template('dashboard.html')
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash("You have been logged out", "info")
    return redirect(url_for('login'))
if __name__==('__main__'):

        
    app.run(debug=True)