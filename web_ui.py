from flask import Flask
from flask import render_template
from flask import url_for
from flask import request


app = Flask(__name__)

@app.route("/")
def form():
    print(url_for('static', filename='css/hello/main.css'))
    return render_template('form.html')

@app.route("/result/", methods=['POST', 'PUT'])
def result():
    print("request.method = ", request.method )
    if request.method == 'POST':
        return render_template('table.html', app_id = request.form['app_id'])

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
