from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user

import utils.queue
from interface.forms import AdminPanelForm, RegistrationForm, LoginForm
from interface.models import User
from extensions import db

blueprint = Blueprint('interface', __name__, template_folder='templates')
queue = utils.queue.Queue()


@blueprint.route('/queue/update', methods=['POST'])
def update():
    print(request.get_json())

    data = request.get_json()
    queue.update_queue(data['queue_length_update'])

    print(queue.waiting_time)
    print(queue.amount_of_people)

    return data, 200


@blueprint.route('/queue/info')
def queue_info():
    response = {'queue_time': queue.waiting_time, 'people_amount': queue.amount_of_people}
    return jsonify(response)


@blueprint.route('/delay/add')  # TODO add a way to add a delay in minutes (or maybe seconds?) to the queue
def add_delay():
    pass


@blueprint.route('/delay/reset')  # TODO add a way to remove the delay
def reset_delay():
    pass


@blueprint.route('/', methods=['GET', 'POST'])
def home():
    form = AdminPanelForm()
    if not current_user.is_authenticated:
        return redirect(url_for('interface.login'))

    if form.validate_on_submit():
        people_amount = form.people_amount.data
        truck_amount = form.truck_amount.data
        queue.update_queue(people_amount)
        queue.update_truck_amount(truck_amount)
        waiting_time = queue.get_waiting_time()
        return render_template('home.html', form=form, waiting_time=waiting_time)

    return render_template('home.html', form=form)


@blueprint.route('/register', methods=['GET', 'POST'])
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
    return redirect(url_for('interface.home'))
