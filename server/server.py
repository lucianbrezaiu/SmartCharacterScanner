from flask import Flask, jsonify, request
from flask_cors import CORS
import json
from sys import argv
from Controller import Controller

app = Flask(__name__)
app.config.from_object(__name__)

CORS(app, resources={r'/*': {'origins': '*'}})

@app.route('/', methods=['GET'])
def home():
    return 'Server is waiting for requests ...'

@app.route('/recognize', methods=['POST'])
def recognize():
    if request.method == 'POST':
        req = json.loads(request.data.decode("utf-8"))
        
        controller = Controller(req)
        response = controller.recognize()
        return jsonify(response)


if __name__ == '__main__':
    try:
        app.debug = True

        port = None
        if len(argv) == 2:
                port = int(argv[1])
        else:
                port = 3000
        print("Server has started on port "+str(port)+".")
        app.run(port=port)
    except Exception as e:
        print("Server exception occurred!: ", str(e))