from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import io
import matplotlib.pyplot as plt
from flask import Response

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
class Expenses(db.Model):
    
    
    id = db.Column(db.Integer, primary_key=True)
    expenses = db.Column(db.String(150), nullable=False)
    money=db.Column(db.Integer, nullable=False)
    time = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(150), nullable=False)

    
    

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

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



@app.route("/delete/<int:id>")
def delete(id):
    expenses = Expenses.query.filter_by(id=id).first()
    db.session.delete(expenses)
    db.session.commit()

    return redirect("/dashboard")

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '').strip()  # Get the search query from the URL

    if not query:
        flash("Please enter a search term.", "warning")
        return redirect('/dashboard')

    # Perform the search (example: search in 'expenses' and 'description' columns)
    search_results = Expenses.query.filter(
        (Expenses.expenses.ilike(f"%{query}%")) | 
        (Expenses.description.ilike(f"%{query}%"))
    ).all()

    # Pass search results to the template
    return render_template('search_results.html', query=query, results=search_results)


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
    
    user_id = session['user_id']  # Get the logged-in user's ID
    
    if request.method == 'POST':
        expense_name = request.form['expenses']
        time = request.form['time']
        money = request.form['money']
        desc = request.form['description']

        new_expense = Expenses(expenses=expense_name,
            time=time,
            money=money, # Use the parsed date
            description=desc,
            user_id=user_id)
        db.session.add(new_expense)
        db.session.commit()
        flash("Expense added successfully", "success")
        
    
    expenses = Expenses.query.filter_by(user_id=user_id).all()
    TotalMoney = sum(expense.money for expense in expenses)

    return render_template('dashboard.html', expenses=expenses,TotalMoney=TotalMoney)
@app.route('/plot/name_pie')
def plot_name_pie():
    expenses = db.session.query(Expenses.expenses, db.func.sum(Expenses.money).label('total_amount'))\
                         .group_by(Expenses.expenses).all()

    labels = [expense.expenses for expense in expenses]
    sizes = [expense.total_amount for expense in expenses]

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=plt.cm.tab20.colors)
    ax.axis('equal')  # Equal aspect ratio ensures the pie is drawn as a circle.

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close(fig)
    return Response(img, mimetype='image/png')


@app.route('/plot/description_pie')
def plot_description_pie():
    expenses = db.session.query(Expenses.description, db.func.sum(Expenses.money).label('total_amount'))\
                         .group_by(Expenses.description).all()

    labels = [expense.description or 'No Description' for expense in expenses]
    sizes = [expense.total_amount for expense in expenses]

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=plt.cm.tab20.colors)
    ax.axis('equal')

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close(fig)
    return Response(img, mimetype='image/png')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash("You have been logged out", "info")
    return redirect(url_for('login'))


@app.route('/visual',methods=["GET",'POST'])
def visual():
    
    expenses = Expenses.query.all()
    return render_template('visuals.html',expenses=expenses)

with app.app_context():
    db.create_all()
if __name__==('__main__'):

        
    app.run(debug=True)