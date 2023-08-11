from uflask import uFlask, make_response, request, render_template
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
        return render_template('index.html')
    else:
        print('ELSE')
        return render_template('index.html')

@app.route('/about')
def about():
    data = 'example'
    print(request.form)
    return render_template('about.html', data = data)

app.run(host = '0.0.0.0', port = 5000)
