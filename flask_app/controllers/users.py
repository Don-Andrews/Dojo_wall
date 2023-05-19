from flask_app.models import user,post
from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def login_n_register_page():
    return render_template("login.html")

@app.route('/register', methods=['POST'])
def register():
    if not user.User.validate_user(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['pword'])
    data = {
        "fname": request.form['fname'],
        "lname": request.form['lname'],
        "email": request.form['email'],
        "pword": pw_hash
    }
    user.User.create_user(data)
    flash("You made a User!", "success")
    return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    data = {"email": request.form["email"]}
    user_check = user.User.select_by_email(data)
    if not user_check:
        flash("Invalid Email/Password", "login")
        return redirect('/')
    if not bcrypt.check_password_hash(user_check.password, request.form["pword"]):
        flash("Invalid Email/Password", "login")
        return redirect('/')
    session["user_id"] = user_check.id
    return redirect('/wall')

@app.route('/wall')
def wall_page():
    if "user_id" not in session:
        return redirect('/')
    data = {"id": session["user_id"]}
    logged_user = user.User.select_by_id(data)
    all_posts = post.Post.all_posts()
    return render_template("dojo_wall.html", user=logged_user, posts=all_posts)

@app.route('/delete/post/<int:post_id>')
def delete_post(post_id):
    data = {"id": post_id}
    post.Post.delete_post(data)
    return redirect('/wall')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/') 