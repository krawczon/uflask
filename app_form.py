from uflask import uFlask, render_template, request, make_response

app = uFlask(__name__)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        print(request.form['username'])
        print(request.form['password'])
        
        # You can perform authentication logic here
        
        return render_template('login.html', data = (username, password))
    return render_template('login.html')

if __name__ == '__main__':
    app.run(port = 5000)
