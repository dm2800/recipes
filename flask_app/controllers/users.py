from flask_app import app

from flask import render_template, redirect, request, session, flash 

from flask_app.models.user import User

from flask_app.models.recipe import Recipe

from flask_bcrypt import Bcrypt


bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/dashboard/')
def dashboard():
    #if user is not logged in, redirect to index. 
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id": session['user_id']
    }
    print(f'printing session id: {session}')
    user = User.get_one(data)
    recipes = Recipe.get_all() 
    users = User.get_all()
    return render_template("dashboard.html", user = user, users = users, recipes = recipes)



@app.route('/user/register/', methods=['POST'])
def register_user():
    is_valid = User.validate_user(request.form)
    if not User.validate_user(request.form):
        return redirect('/')
    new_user = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email' : request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password'])
    }
    print(f'printing new_user: {new_user}')
    id = User.save(new_user)
    if not id:
        flash ('Something went wrong')
        return redirect ('/')
    session['user_id'] = id
    flash("You are now logged in", "login")
    return redirect ('/dashboard/')




@app.route('/logout/')
def logout():
    session.clear()
    return redirect('/')


@app.route('/user/login/', methods=['POST'])
def login():
    if len(request.form['password']) < 1:
        flash('Please enter password', 'login')
        return redirect("/")
    
    data = { 
        "email" : request.form["email"] 
    }
    # see if the email provided exists in the database
    user_in_db = User.get_by_email(request.form)
    # if user is not registered in the db
    if not user_in_db:
        flash("That email is not in our database-- please register.", "login")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        # if we get False after checking the password
        flash("Invalid Password", "login")
        return redirect('/')
    
    # if the passwords matched, we set the user_id into session
    session['user_id'] = user_in_db.id
    flash('You are now logged in.')
    # never render on a post!!!
    return redirect("/dashboard/")