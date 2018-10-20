from flask import *
app = Flask(__name__)

@app.route('/fires', methods=['GET', 'POST'])
def fires():
    if request.method == 'POST':
        return report_fire()
    else:
        return find_fires()

def report_fire():
    print(request.json)
    return ('', 201)

def find_fires():
    return ('hello', 200)