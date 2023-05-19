from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User
from flask import flash


class Post:
    def __init__(self, data):
        self.id = data['id']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = None

    @classmethod
    def create_post(cls, data):
        query = "INSERT INTO posts (content, created_at, updated_at, users_id) \
                VALUES (%(content)s, NOW(), NOW(), %(uid)s);"
        result = connectToMySQL('dojo_wall_schema').query_db(query, data)
        return result
    
    @classmethod
    def all_posts(cls):
        query = "SELECT * FROM posts JOIN users ON \
                posts.users_id=users.id;"
        result = connectToMySQL('dojo_wall_schema').query_db(query)
        posts = []
        for row in result:
            post = cls(row)
            user_data = {
                "id": row["users.id"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "email": row["email"],
                "password": row["password"],
                "created_at": row["users.created_at"],
                "updated_at": row["users.updated_at"]
            }
            user_object = User(user_data)
            post.user = user_object
            posts.append(post)
        return posts
    
    @classmethod
    def delete_post(cls, data):
        query = "DELETE FROM posts WHERE id=%(id)s"
        result = connectToMySQL('dojo_wall_schema').query_db(query, data)
        return result
    
    @staticmethod
    def validate_post(data):
        is_valid = True
        if len(data['content']) == 0:
            flash("Content box cannot be blank!", "posts")
            is_valid = False
        return is_valid