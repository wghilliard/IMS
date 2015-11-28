from app import app, db, lm
from flask import render_template, flash, redirect, url_for, request, session
from .forms import LoginForm
from .models import User


@lm.user_loader
def load_user(id):
    user = User.objects(pk=id).first()
    if user:
        return user
    else:
        return None


@app.route('/', methods=['GET'])
def default():
    return render_template('index.html')

#

# @app.route('/')
# @app.route('/index')
# @login_required
# def index():
#     user = {'nickname': 'Miguel'}
#     posts = [  # fake array of posts
#         {
#             'author': {'nickname': 'John'},
#             'body': 'Beautiful day in Portland!'
#         },
#         {
#             'author': {'nickname': 'Susan'},
#             'body': 'The Avengers movie was so cool!'
#         }
#     ]
#     return render_template('index.html', title='Home',
#                            user=user, posts=posts)
#

# @app.route('/logout')
# @login_required
# def logout():
#     """Logout the current user."""
#     user = current_user
#     user.authenticated = False
#     user.save()
#     logout_user()
#     form = LoginForm()
#     return render_template('login.html',
#                            title='Sign In',
#                            form=form)
