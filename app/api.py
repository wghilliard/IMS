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
    # IMS/app/templates/app/index.html
    return render_template('index.html')


@app.route('/api/username', methods=['POST'])
def check_username():
    try:
        # print dir(request.form)
        # print vars(request.form)
        # print request.form['username']
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
        return jsonify({'username': user.username,
                        'action': 'who_am_i',
                        'status': 'success'})
    except AttributeError:
        return jsonify({'username': 'anonymous',
                        'action': 'who_am_i',
                        'status': 'success'})


@app.route('/api/login', methods=['POST'])
def check_password():
    # TODO: Change from form to JSON
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
    # print request.form['username']
    # print request.form['password']

    user = User.objects(username=request.form['username']).first()

    if user:
        return jsonify({'status': 'failed',
                        'error': 'username_exists',
                        'action': 'register'})
    else:
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
def delete_user():
    loaded_data = json.loads(request.data)
    user_object = User.objects(username=loaded_data['username']).first()
    print user_object.password
    print loaded_data
    if bcrypt.check_password_hash(user_object.password, loaded_data['password']):
        logout_user()
        print "in"
        try:
            user_object.delete()
            return jsonify({'status': 'success',
                            'action': 'delete_user'})
        except Exception as e:
            print e
            return jsonify({'status': 'failed',
                            'action': 'delete_user'})
    else:
        print 'failed'
        return jsonify({'status': 'failed',
                        'error': 'bad password',
                        'action': 'delete_user'})


@app.route('/api/generate', methods=['POST', 'GET'])
@login_required
def generate():
    if current_user:

        # Check status of schedule generation.
        if request.method == 'GET':
            try:
                if session.get('gen_id'):
                    # print session['gen_id']
                    gen_object = Generator.objects(pk=session['gen_id']).first()
                    if gen_object:
                        if gen_object.status['fetch'] == 'started':
                            return jsonify({'status': 'busy',
                                            'action': 'fetching'})

                        elif gen_object.status['fetch'] == 'failed':
                            session['gen_id'] = ''
                            return jsonify({'status': 'failed',
                                            'action': 'fetching',
                                            'error': gen_object.error})

                        elif gen_object.status['compile'] == 'waiting':
                            return jsonify({'status': 'working',
                                            'action': 'generate'})

                        elif gen_object.status['compile'] == 'failed':
                            print "sending error"
                            session['gen_id'] = ''
                            return jsonify({'status': 'failed',
                                            'action': 'generate',
                                            'error': gen_object.error})

                        elif gen_object.status['compile'] == 'complete':
                            session['gen_id'] = ''
                            return jsonify({'status': 'complete',
                                            'action': 'generate',
                                            'schedules': get_schedules()})
                    else:
                        session['gen_id'] = ''
                        return jsonify({'status': 'not_started',
                                        'action': 'get_generate'})

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
                # print session.get('gen_id')
                return jsonify({'status': 'busy',
                                'action': 'generate'})
            try:
                loaded_data = json.loads(request.data)
                print loaded_data
                gen_object = Generator(owner=current_user.id, classes=loaded_data['classes'],
                                       status={'fetch': 'started', 'compile': 'waiting'},
                                       block_outs=loaded_data['block_outs']).save()
                session['gen_id'] = str(gen_object.id)
                parse.delay(gen_object.id, loaded_data)
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
    session['gen_id'] = None
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
    # print final_list
    return final_list


@app.route('/api/schedules/<string:sched_id>')
@login_required
def delete_sched(sched_id):
    try:
        user_object = User.objects(pk=current_user.id).first()
        schedule_object = Schedule.objects(pk=sched_id).first()
        if schedule_object:
            user_object.schedules.remove(schedule_object.id)
            user_object.save()
            schedule_object.delete()
            return jsonify({'status': 'success',
                            'id': sched_id,
                            'action': 'delete_schedule'})
    except Exception as e:
        print e
        return jsonify({'status': 'failed',
                        'id': sched_id,
                        'action': 'delete_schedule'})
