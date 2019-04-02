from flask import Flask, request, jsonify
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/v1/staging/myapp', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return jsonify({"status": "ok"})
    else:
        return "Received GET"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
