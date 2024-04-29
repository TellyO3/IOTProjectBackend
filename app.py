from flask import Flask, request

app = Flask(__name__)

global count
count = 0


@app.route("/update", methods=['POST'])
def update():
    global count

    print(request.get_json())

    data = request.get_json()
    count += data['queue_length_update']

    print(count)

    return data, 200


if __name__ == '__main__':
    app.run()
