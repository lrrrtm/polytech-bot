from flask import Flask, request, jsonify
from sender import send_feedback

app = Flask(__name__)


@app.route('/send_feedback', methods=['POST'])
def feedback():
    data = request.json
    send_feedback(data['params'])

    response = {
        'status': 'success',
        'message': 'Feedback received!'
    }
    return jsonify(response), 201


if __name__ == '__main__':
    app.run(port=5000)
