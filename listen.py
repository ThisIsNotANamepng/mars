from flask import Flask, request

app = Flask(__name__)

global registeredIDs
global registeredTypes

@app.route('/')
def hello():
    return 'Active'

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        print(request)
        id = request.values.get('id')
        type = request.values.get('type')
    else:
        return 'Invalid request method'
    return " "


app.run(host='0.0.0.0', port=5600)