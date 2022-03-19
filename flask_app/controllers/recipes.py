
from flask import render_template, redirect, session, request, flash
from flask_app import app 
from flask_app.models.recipe import Recipe
from flask_app.models.user import User



@app.route('/recipes/new/')
def add_recipe():
    if 'user_id' not in session:
        flash("You must be logged in to view this page")
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    return render_template('new.html', user=User.get_one(data))


@app.route('/recipes/create/', methods=['POST'])
def create_recipe():
    if 'user_id' not in session:
        flash("You must be logged in to view this page", "register")
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    if not Recipe.validate_recipe(request.form):
        return redirect ('/recipes/new/')
    data = {
        "name": request.form["name"],
        "description": request.form["description"],
        "instructions": request.form["instructions"],
        "date_made": request.form["date_made"],
        "under_30_mins": request.form["under_30_mins"],
        "user_id": session['user_id']
    }
    Recipe.save(data)
    return redirect('/dashboard/')

# @app.route('/recipes/create/<int:recipe_id>/', methods=['POST'])
# def create_recipe(recipe_id):
#     if not Recipe.validate_recipe(request.form):
#         return redirect ('/dashboard/')
#     data = {
#         "id": recipe_id,
#         "name": request.form["name"],
#         "description": request.form["description"],
#         "instructions": request.form["instructions"],
#         "date_made": request.form["date_made"],
#         "under_30_mins": request.form["under_30_mins"]
#     }
#     Recipe.save(data)
#     return redirect('/dashboard/')

@app.route('/recipes/view/<int:recipe_id>/')
def view_recipe(recipe_id):
    if 'user_id' not in session:
        flash("You must be logged in to view this page")
        return redirect('/')
    userData = {
        'id': session['user_id']
    }
    data = {
        'id': recipe_id
    }
    return render_template('view.html', recipe=Recipe.get_one_recipe(data), user=User.get_one(userData))


@app.route('/recipes/edit/<int:recipe_id>/')
def edit_recipe(recipe_id):
    data = {
        "id": recipe_id
    }
    recipe = Recipe.get_one_recipe(data)
    return render_template("edit.html", recipe =recipe)

@app.route('/recipes/update/<int:recipe_id>/', methods=['POST'])
def update_recipe(recipe_id):
    if not Recipe.validate_recipe(request.form):
        return redirect (f'/recipes/edit/{recipe_id}/')
    data = {
        "id": recipe_id,
        "name": request.form["name"],
        "description": request.form["description"],
        "instructions": request.form["instructions"],
        "date_made": request.form["date_made"],
        "under_30_mins": request.form["under_30_mins"]
    }
    Recipe.update(data)
    return redirect ("/dashboard/")

@app.route('/recipes/destroy/<int:recipe_id>/')
def delete (recipe_id):
    data = {
        "id": recipe_id
    }
    Recipe.delete(data)
    return redirect("/dashboard/")


    


