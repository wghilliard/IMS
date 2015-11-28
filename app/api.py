from flask import send_file, jsonify, make_response, request, session
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, bcrypt
from models import *
from mongoengine.errors import *
from bson.objectid import ObjectId
from scraper.core import parse


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = User.objects(username=form.username.data).first()
#         if user:
#             if form.password.data in user.password:
#                 user.authenticated = True
#                 user.save()
#                 login_user(user)
#             # session['remember_me'] = form.remember_me.data
#             # flash('Login requested for Username="%s", remember_me=%s' %
#             #       (form.username.data, str(form.remember_me.data)))
#                 return redirect(url_for('index'))
#     return render_template('login.html',
#                            title='Sign In',
#                            form=form)


@app.route('/api/username', methods=['POST'])
def check_username():
    try:
        user = User.objects(username=request.form['username']).first()
    except Exception as e:
        app.logger.error('Uncaught error: {0}'.format(e))
        return jsonify({'error': 'unknown',
                        'status': 'failed',
                        'action': 'username_check'})
    if user:
        return jsonify({'status': 'complete',
                        'action': 'username_check'})
    else:
        return jsonify({'status': 'none',
                        'action': 'username_check'})


@app.route('/api/who', methods=['GET'])
def who_am_i():
    try:
        user = current_user
        return jsonify({'user': user.username,
                        'action': 'who_am_i'})
    except AttributeError:
        return jsonify({'user': 'anonymous',
                        'action': 'who_am_i'})


@app.route('/api/login', methods=['POST'])
def check_password():
    user = User.objects(username=request.form['username']).first()
    if not user:
        return jsonify({'status': 'failed',
                        'error': 'username_not_exist',
                        'action': 'login'})

    if bcrypt.check_password_hash(user.password, request.form['password']):
        login_user(user)
        return jsonify({'status': 'complete',
                        'action': 'login'})
    else:
        return jsonify({'status': 'failed',
                        'action': 'login'})


@app.route('/api/register', methods=['POST'])
def register_user():
    user = User.objects(username=request.form['username']).first()

    if user:
        return jsonify({'status': 'failed',
                        'error': 'username_exists',
                        'action': 'register'})

    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    user = User(username=request.form['username'], password=pw_hash)

    if user.save():
        login_user(user)
        return jsonify({'status': 'complete',
                        'action': 'register_user'})
    else:
        return jsonify({'status': 'failed',
                        'action': 'register_user'})


@app.route('/api/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return jsonify({'status': 'complete',
                    'action': 'logout'})


# @app.route('/api/test', methods=['GET'])
# def test():
#     Schedule().save()
#     thing = Schedule.objects().first()
#     return jsonify({'data': [thing.name for thing in Schedule.objects()]})


# TODO: ValidationError: u'None' is not a valid ObjectId, it must be a 12-byte input or a 24-character hex string
@app.route('/api/delete', methods=['POST'])
@login_required
def delete_user():
    user = User(username=request.form['username'], password=request.form['password'])

    logout_user()
    if user.delete():
        return jsonify({'status': 'complete',
                        'action': 'delete_user'})
    else:
        return jsonify({'status': 'failed',
                        'action': 'delete_user'})


@app.route('/api/generate', methods=['POST', 'GET'])
def generate():
    # Check status of schedule generation.
    if request.method == 'GET':
        # gen_id = session.get('gen_id')
        # schedule_object = Schedule.objects(pk=gen_id).first()

        # return jsonify({'status': schedule_object.status,
        #                 'name': schedule_object.name})
        return jsonify({'test': 'true'})
    elif request.method == 'POST':

        # schedule_object = Schedule().save()
        # session['gen_id'] = schedule_object.id
        parse.delay([['MATH', '3330'],
                     ['CSE', '1301']])
        return jsonify({'status': 'started'})

    else:
        print(request.method)
        return jsonify({'fuck': 'true'})
