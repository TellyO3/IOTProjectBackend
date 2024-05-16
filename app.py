from flask import request

import init
import queue

app = init.create_app()
queue = queue.Queue()


@app.route('/queue/update', methods=['POST'])
def update():
    print(request.get_json())

    data = request.get_json()
    queue.modify_queue(data['queue_length_update'])

    print(queue.waiting_time)
    print(queue.length)

    return data, 200


@app.route('/queue/info')  # TODO retrieve information about the queue via the api
def queue_info():
    pass


@app.route('/delay/add')  # TODO add a way to add a delay in minutes (or maybe seconds?) to the queue
def add_delay():
    pass


@app.route('/delay/reset')  # TODO add a way to remove the delay
def reset_delay():
    pass


@app.route('/')  # TODO simple overview page for the managers of the zoo
def interface():
    pass


if __name__ == '__main__':
    app.run()
