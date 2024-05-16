from flask import Blueprint, request, jsonify, render_template
import utils.queue
from interface.forms import PeopleInputForm

interface = Blueprint('interface', __name__, template_folder='templates')
queue = utils.queue.Queue()


@interface.route('/queue/update', methods=['POST'])
def update():
    print(request.get_json())

    data = request.get_json()
    queue.update_queue(data['queue_length_update'])

    print(queue.waiting_time)
    print(queue.amount_of_people)

    return data, 200


@interface.route('/queue/info')
def queue_info():
    response = {'queue_time': queue.waiting_time, 'people_amount': queue.amount_of_people}
    return jsonify(response)


@interface.route('/delay/add')  # TODO add a way to add a delay in minutes (or maybe seconds?) to the queue
def add_delay():
    pass


@interface.route('/delay/reset')  # TODO add a way to remove the delay
def reset_delay():
    pass


@interface.route('/', methods=['GET', 'POST'])
def home():
    form = PeopleInputForm()

    if form.validate_on_submit():
        amount = form.amount.data
        queue.update_queue(amount)
        waiting_time = queue.get_waiting_time()
        return render_template('home.html', form=form, waiting_time=waiting_time)

    return render_template('home.html', form=form)
