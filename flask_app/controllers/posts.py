from flask_app.models import user,post
from flask_app import app
from flask import render_template, redirect, request, session, flash

@app.route('/post', methods=['POST'])
def create_post():
    if not post.Post.validate_post(request.form):
        return redirect('/wall')
    post.Post.create_post(request.form)
    return redirect('/wall')