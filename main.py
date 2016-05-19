from datetime import datetime
from flask import Flask
from flask import render_template
from flask import url_for
from flask import request, make_response
from flask import send_from_directory
import flask
import intercom

app = Flask(__name__)

result_file_path = './static/result.csv'
csv_result = ''

@app.route("/")
def form():
    return render_template('form.html')

@app.route("/result", methods=['POST', 'PUT'])
def result():
    try:
        print("request.method = ", request.method )
        print("request.form = ", request.form )

        if request.method == 'POST':
            global csv_result
            from_date = datetime.strptime(request.form['from_date'], '%Y.%m.%d')
            to_date = datetime.strptime(request.form['to_date'], '%Y.%m.%d')
            app_id = request.form['app_id']
            api_key = request.form['api_key']
            conv_parts = intercom.get_conversation_parts(from_date, to_date, app_id, api_key)
            conv_parts_dict = intercom.prepare_conv_parts(conv_parts, 'dict')
            csv_result = intercom.prepare_conv_parts(conv_parts, 'csv')
            # fl = open(result_file_path, 'w')
            # fl.write(conv_parts_csv)
            # fl.close()
            # print(conv_parts)
            return render_template('table.html', conv_parts=conv_parts_dict, err = 'No records found')
    except ValueError:
        err_str = 'Wrong request to intercom. Please Check App ID and APIkey'
        return render_template('table.html', conv_parts=[], err = err_str)


@app.route('/csv')
def download_file():
    response = make_response(csv_result)
    # This is the key: Set the right header for the response
    # to be downloaded, instead of just printed on the browser
    response.headers["Content-Disposition"] = "attachment; filename=result.csv"
    response.headers["Content-type"] = "text/csv"
    return response

    # return send_from_directory(app.static_folder, 'result.csv', as_attachment=True)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
