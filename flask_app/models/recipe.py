from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User
from flask import flash


class Recipe:
    db = 'recipes_schema'
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.under_30_mins = data['under_30_mins']
        self.created_at = data['created_at']
        self.updated = data['updated_at']
        self.user_id = data['user_id']
        self.users = []

    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        if len(recipe['name']) < 5: 
            flash('Name must be at least 3 characters', "error")
            is_valid = False
        if len(recipe['description']) < 5: 
            flash('Description must be at least 3 characters', "error")
            is_valid = False
        if len(recipe['instructions']) < 5: 
            flash('Instructions must be at least 3 characters', "error")
            is_valid = False
        return is_valid 

    @classmethod    
    def get_one_recipe(cls,data):
        query = 'SELECT * FROM recipes where id = %(id)s'
        results = connectToMySQL(cls.db).query_db(query,data)
        print(f'printing one recipe results: {results}')
        if len(results)<1:
            return False
        return cls(results[0])

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes;"
        recipes_from_db = connectToMySQL(cls.db).query_db(query)
        recipes =[]
        for row in recipes_from_db:
            recipes.append(cls(row))
        print(f'printing all recipes: {recipes}')
        return recipes

    @classmethod
    def get_recipe_with_users(cls, data):
        query = "SELECT * FROM recipes LEFT JOIN users ON recipes.user_id = users.id WHERE user_id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        # RESULTS WILL BE A LIST OF recipe OBJECTS WITH THE user ATTACHED TO EACH ROW. 
        print (f'printing recipe results: {results}')
        recipe = cls(results[0])
        for row_from_db in results: 
            user_data = {
                "id" : row_from_db["users.id"],
                "first_name" : row_from_db["first_name"],
                "last_name" : row_from_db["last_name"],
                "email" : row_from_db["email"],
                "password" : row_from_db["password"],
                "created_at" : row_from_db["users.created_at"], 
                "updated_at" : row_from_db["users.updated_at"]
            }
            recipe.users.append(User(user_data ) )
        return recipe 


    @classmethod
    def delete(cls,data):
        query = "DELETE FROM recipes where id = %(id)s"
        return connectToMySQL(cls.db).query_db(query,data)
    @classmethod
    def update(cls,data):
        query = "UPDATE recipes SET name = %(name)s, description =  %(description)s,  instructions = %(instructions)s, date_made = %(date_made)s, under_30_mins = %(under_30_mins)s, updated_at = NOW() WHERE id = %(id)s"
        return connectToMySQL(cls.db).query_db(query,data)
    @classmethod
    def save (cls, data):
        query = "INSERT INTO recipes (name, description, instructions, date_made, under_30_mins, created_at, updated_at, user_id) "\
                "VALUES (%(name)s, %(description)s, %(instructions)s, %(date_made)s, %(under_30_mins)s, NOW(), NOW(), %(user_id)s)"
        return connectToMySQL(cls.db).query_db(query,data)
