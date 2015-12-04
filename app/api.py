from flask import send_file, jsonify, make_response, request, session, render_template
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, bcrypt, lm
from models import *
from mongoengine.errors import *
from bson.objectid import ObjectId
import json
from werkzeug.exceptions import *
from scraper.core import parse, compile_schedules


# from matt_code.core import compile_schedules
# from app import app, db, lm


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
        return jsonify({'status': 'success',
                        'action': 'username_check'})
    else:
        return jsonify({'status': 'none',
                        'action': 'username_check'})


@app.route('/api/who', methods=['GET'])
def who_am_i():
    try:
        user = current_user
        session['gen_id'] = None
        return jsonify({'user': user.username,
                        'action': 'who_am_i',
                        'status': 'success'})
    except AttributeError:
        return jsonify({'user': 'anonymous',
                        'action': 'who_am_i',
                        'status': 'success'})


@app.route('/api/login', methods=['POST'])
def check_password():
    user = User.objects(username=request.form['username']).first()
    if not user:
        return jsonify({'status': 'failed',
                        'error': 'username_not_exist',
                        'action': 'login'})

    if bcrypt.check_password_hash(user.password, request.form['password']):
        login_user(user)
        return jsonify({'status': 'success',
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
        return jsonify({'status': 'success',
                        'action': 'register_user'})
    else:
        return jsonify({'status': 'failed',
                        'action': 'register_user'})


@app.route('/api/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return jsonify({'status': 'success',
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
        return jsonify({'status': 'success',
                        'action': 'delete_user'})
    else:
        return jsonify({'status': 'failed',
                        'action': 'delete_user'})


@app.route('/api/generate', methods=['POST', 'GET'])
@login_required
def generate():
    if current_user:

        # Check status of schedule generation.
        if request.method == 'GET':
            try:
                if session.get('gen_id'):
                    print session['gen_id']
                    gen_object = Generator.objects(pk=session['gen_id']).first()
                    if gen_object.status['fetch'] != 'complete':
                        return jsonify({'status': 'busy',
                                        'action': 'fetching'})
                    elif gen_object.status['compile'] == 'failed':
                        session['gen_id'] = ''
                        return jsonify({'status': 'failed',
                                        'action': 'generate',
                                        'error': gen_object.error})

                    elif gen_object.status['compile'] == 'complete':

                        return jsonify({'status': 'complete',
                                        'action': 'generate',
                                        'schedules': get_schedules()})
                else:
                    return jsonify({'status': 'not_started',
                                    'action': 'get_generate'})

            # schedule_object = Schedule.objects(pk=gen_id).first()

            # return jsonify({'status': schedule_object.status,
            #                 'name': schedule_object.name})
            except Exception as e:
                print e
                raise BadRequest

        elif request.method == 'POST':
            # print request.data
            if session.get('gen_id'):
                return jsonify({'status': 'busy',
                                'action': 'generate'})
            try:
                loaded_data = json.loads(request.data)
                gen_object = Generator(owner=current_user.id, classes=loaded_data['classes'],
                                       status={'fetch': 'started', 'compile': 'waiting'},
                                       block_outs=loaded_data['block_outs']).save()
                session['gen_id'] = str(gen_object.id)
                parse(gen_object.id, loaded_data)
                # compile_schedules(loaded_data, gen_object.id)
                return jsonify({'status': 'started',
                                'action': 'generate'})
            except Exception as e:
                print e
                raise BadRequest

    else:
        print(request.method)
        return jsonify({'fuck': 'true'})


@app.route('/api/schedules', methods=['GET'])
@login_required
def serve_schedules():
    return jsonify({'status': 'complete',
                    'action': 'serve_schedules',
                    'schedules': get_schedules()})


def get_schedules():
    sched_list = User.objects(pk=current_user.id).first().schedules
    # session['gen_id'] = ''
    final_list = list()
    for item in sched_list:
        final_list.append(Schedule.objects(pk=item).first().to_mongo().to_dict())

    for item in final_list:
        # print item
        item['_id'] = str(item['_id'])
        item['sections'] = None
    print final_list
    return final_list
