from flask import Flask, render_template, redirect, url_for, request
from flask_wtf import FlaskForm
from requests.exceptions import ConnectionError
from wtforms import IntegerField, StringField, DecimalField
from wtforms.validators import DataRequired

import urllib.request
import json


class ClientDataForm(FlaskForm):
    Sex = StringField('Sex', validators=[DataRequired()])
    ChestPainType = StringField('ChestPainType', validators=[DataRequired()])
    RestingECG = StringField('RestingECG', validators=[DataRequired()])
    ExerciseAngina = StringField('ExerciseAngina', validators=[DataRequired()])
    ST_Slope = StringField('ST_Slope', validators=[DataRequired()])
    Age = IntegerField('Age', validators=[DataRequired()])
    RestingBP = IntegerField('RestingBP', validators=[DataRequired()])
    Cholesterol = IntegerField('Cholesterol', validators=[DataRequired()])
    FastingBS = IntegerField('FastingBS', validators=[DataRequired()])
    MaxHR = IntegerField('MaxHR', validators=[DataRequired()])
    Oldpeak = DecimalField('Oldpeak', validators=[DataRequired()])


app = Flask(__name__)
app.config.update(
    CSRF_ENABLED=True,
    SECRET_KEY='you-will-never-guess',
)


def get_prediction(Sex, ChestPainType, RestingECG, ExerciseAngina, ST_Slope, Age, RestingBP, Cholesterol, FastingBS, MaxHR, Oldpeak):
    body = {'Sex': Sex,
            'ChestPainType': ChestPainType,
            'RestingECG': RestingECG,
            'ExerciseAngina': ExerciseAngina,
            'ST_Slope': ST_Slope,
            'Age': Age,
            'RestingBP': RestingBP,
            'Cholesterol': Cholesterol,
            'FastingBS': FastingBS,
            'MaxHR': MaxHR,
            'Oldpeak': Oldpeak}

    myurl = "http://0.0.0.0:8180/predict"
    req = urllib.request.Request(myurl)
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    jsondata = json.dumps(body)
    jsondataasbytes = jsondata.encode('utf-8')  # needs to be bytes
    req.add_header('Content-Length', len(jsondataasbytes))
    # print(jsondataasbytes)
    response = urllib.request.urlopen(req, jsondataasbytes)
    return json.loads(response.read())['predictions']


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/predicted/<response>')
def predicted(response):
    response = json.loads(response)
    print(response)
    return render_template('predicted.html', response=response)


@app.route('/predict_form', methods=['GET', 'POST'])
def predict_form():
    form = ClientDataForm()
    data = dict()
    if request.method == 'POST':
        data['Sex'] = request.form.get('Sex')
        data['ChestPainType'] = request.form.get('ChestPainType')
        data['RestingECG'] = request.form.get('RestingECG')
        data['ExerciseAngina'] = request.form.get('ExerciseAngina')
        data['ST_Slope'] = request.form.get('ST_Slope')
        data['Age'] = request.form.get('Age')
        data['RestingBP'] = request.form.get('RestingBP')
        data['Cholesterol'] = request.form.get('Cholesterol')
        data['FastingBS'] = request.form.get('FastingBS')
        data['MaxHR'] = request.form.get('MaxHR')
        data['Oldpeak'] = request.form.get('Oldpeak')

        try:
            response = str(get_prediction(data['Sex'],
                                          data['ChestPainType'],
                                          data['RestingECG'],
                                          data['ExerciseAngina'],
                                          data['ST_Slope'],
                                          data['Age'],
                                          data['RestingBP'],
                                          data['Cholesterol'],
                                          data['FastingBS'],
                                          data['MaxHR'],
                                          data['Oldpeak']))
            print(response)
        except ConnectionError:
            response = json.dumps({"error": "ConnectionError"})
        return redirect(url_for('predicted', response=response))
    return render_template('form.html', form=form)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8181, debug=True)
