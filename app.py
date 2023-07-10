from uflask import uFlask, make_response, request
from render_template import render_template
#import machine
import time

app = uFlask(__name__)

session = {}

@app.route('/', methods = ['GET'])
def home():
    if request.method == 'GET':
        return render_template('index.html', data = 'data from uflask app')

@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        session['data'] = request.form['value']
        return render_template('index.html')
    else:
        print('ELSE')
        return render_template('index.html')

@app.route('/about')
def about():
    print(request.form)
    return render_template('about.html')


if __name__ == '__main__':
    app.run(port=5000)
