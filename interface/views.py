from flask import Blueprint, request, jsonify, render_template, redirect, url_for, current_app
from flask_login import login_user, login_required, logout_user

import utils.queue
from interface.forms import AdminPanelForm, RegistrationForm, LoginForm, SettingsForm
from interface.models import User, Settings
from extensions import db, csrf

blueprint = Blueprint('interface', __name__, template_folder='templates')
queue = utils.queue.Queue()


@blueprint.route('/display', methods=['GET'])
@csrf.exempt
def queue_display():
    wachttijd = queue.get_waiting_time()
    response = {
        'wachttijd': wachttijd,
    }
    return jsonify(response)


@blueprint.route('/queue/update', methods=['POST'])
@csrf.exempt
def update():
    print(request.get_json())

    data = request.get_json()
    queue.update_queue(data['queue_length_update'])

    print(queue.waiting_time)
    print(queue.amount_of_people)

    return data, 200


@blueprint.route('/queue/info')
def queue_info():
    response = {'queue_time': queue.waiting_time, 'change_people': queue.amount_of_people}
    return jsonify(response)


@blueprint.route('/delay/change', methods=['POST'])
@csrf.exempt
def change_delay():
    data = request.get_json()
    queue.change_delay(data['delay_change'])

    print(queue.delay_amount)

    return data, 200


@blueprint.route('/delay/reset')
def reset_delay():
    queue.reset_delay()


@blueprint.route('/', methods=['GET', 'POST'])
@login_required
def home():
    form = AdminPanelForm()

    if form.validate_on_submit():
        queue.update_queue(form.change_people.data)
        with current_app.app_context():
            settings_data = Settings.query.first()
            if settings_data:
                queue.truck_count = settings_data.truck_count
                queue.delay_amount = settings_data.delay

        queue.update_waiting_time()
        waiting_time = queue.get_waiting_time()
        people_amount = queue.get_people_amount()

        return render_template('home.html', form=form,
                               waiting_time=waiting_time,
                               people_amount=people_amount)

    with current_app.app_context():
        settings_data = Settings.query.first()
        if settings_data:
            queue.truck_count = settings_data.truck_count
            queue.delay_amount = settings_data.delay
    queue.update_waiting_time()
    waiting_time = queue.get_waiting_time()
    people_amount = queue.get_people_amount()

    return render_template('home.html', form=form,
                           waiting_time=waiting_time,
                           people_amount=people_amount)


@blueprint.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('interface.home'))
    return render_template('register.html', form=form)


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if not User.query.first():
        return redirect(url_for('interface.setup'))

    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user is not None and user.check_password(form.password.data):
                login_user(user)
                next = request.args.get('next')
                if next is None or not next[0] == '/':
                    next = url_for('interface.home')
                    return redirect(next)

    return render_template('login.html', form=form)


@blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('interface.login'))


@blueprint.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    form = SettingsForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            with current_app.app_context():
                settings_data = Settings.query.first()
                if settings_data:
                    settings_data.truck_count = form.truck_count.data
                    settings_data.delay = form.delay_amount.data
                db.session.add(settings_data)
                db.session.commit()

            queue.update_truck_amount(form.truck_count.data)
            queue.change_delay(form.delay_amount.data)
            return redirect(url_for('interface.home'))
        return render_template('settings.html', form=form)
    return render_template('settings.html', form=form)


@blueprint.route('/setup', methods=['GET', 'POST'])
def setup():
    form = RegistrationForm()

    if not User.query.first():
        if form.validate_on_submit():
            user = User(username=form.username.data,
                        password=form.password.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('interface.login'))

        return render_template('setup.html', form=form)

    else:
        return redirect(url_for('interface.login'))
