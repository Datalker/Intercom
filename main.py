from datetime import datetime
from flask import Flask
from flask import render_template
from flask import url_for
from flask import request
from flask import send_from_directory
import intercom

app = Flask(__name__)

result_file_path = './static/result.csv'

@app.route("/")
def form():
    return render_template('form.html')

@app.route("/result", methods=['POST', 'PUT'])
def result():
    print("request.method = ", request.method )
    print("request.form = ", request.form )

    if request.method == 'POST':
        from_date = datetime.strptime(request.form['from_date'], '%Y.%m.%d')
        to_date = datetime.strptime(request.form['to_date'], '%Y.%m.%d')
        app_id = request.form['app_id']
        api_key = request.form['api_key']
        conv_parts = intercom.get_conversation_parts(from_date, to_date, app_id, api_key)
        conv_parts_dict = intercom.prepare_conv_parts(conv_parts, 'dict')
        conv_parts_csv = intercom.prepare_conv_parts(conv_parts, 'csv')
        fl = open(result_file_path, 'w')
        fl.write(conv_parts_csv)
        fl.close()
        # print(conv_parts)
        return render_template('table.html', conv_parts=conv_parts_dict)

@app.route('/csv')
def download_file():
    return send_from_directory(app.static_folder, 'result.csv', as_attachment=True)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
