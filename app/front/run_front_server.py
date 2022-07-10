from flask import Flask, render_template, redirect, url_for, request
from flask_wtf import FlaskForm
from requests.exceptions import ConnectionError
from wtforms import IntegerField, DecimalField
from wtforms.validators import DataRequired

import urllib.request
import json


class ClientDataForm(FlaskForm):
    Sex = IntegerField('Sex (Value: Male = 1, Female = 0)', validators=[DataRequired()])
    AnginaPectoris = IntegerField('AnginaPectoris (Value: Yes = 1; No = 0)', validators=[DataRequired()])
    Vessels = IntegerField('Vessels (Value: 0-2)', validators=[DataRequired()])
    Chest_Pain_Type = IntegerField('Chest_Pain_Type (Value: 0-3)', validators=[DataRequired()])
    Sugar_level = IntegerField('Sugar_level (Value fasting blood sugar > 120 mg/dl: True = 1; False = 0)',
                               validators=[DataRequired()])
    Electrocardiographic = IntegerField('Electrocardiographic (Value: 0-2)', validators=[DataRequired()])
    Slope = IntegerField('Slope (Value: 0-2)', validators=[DataRequired()])
    Thal_Rate = IntegerField('Thal_Rate (Value: 1-3)', validators=[DataRequired()])
    Age = IntegerField('Age (Integer Number)', validators=[DataRequired()])
    Pressure = IntegerField('Pressure (Integer Number)', validators=[DataRequired()])
    Cholesterol = IntegerField('Cholesterol (Integer Number)', validators=[DataRequired()])
    Max_Heart_Rate = IntegerField('Max_Heart_Rate (Integer Number)', validators=[DataRequired()])
    Old_Peak = DecimalField('Old_Peak (Decimal number)', validators=[DataRequired()])


app = Flask(__name__)
app.config.update(
    CSRF_ENABLED=True,
    SECRET_KEY='you-will-never-guess',
)


def get_prediction(Sex, AnginaPectoris, Vessels, ChestPainType, SugarLevel, Electrocardiographic, Slope, ThalRate,
                   Age, Pressure, Cholesterol, MaxHeartRate, OldPeak):
    body = {'Sex': Sex,
            'Angina_pectoris': AnginaPectoris,
            'Vessels': Vessels,
            'Chest_Pain_Type': ChestPainType,
            'Sugar_level': SugarLevel,
            'Electrocardiographic': Electrocardiographic,
            'Slope': Slope,
            'Thal_Rate': ThalRate,
            'Age': Age,
            'Pressure': Pressure,
            'Cholesterol': Cholesterol,
            'Max_Heart_Rate': MaxHeartRate,
            'Old_Peak': OldPeak}

    myurl = "http://0.0.0.0:8180/predict"
    req = urllib.request.Request(myurl)
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    jsondata = json.dumps(body)
    jsondataasbytes = jsondata.encode('utf-8')
    req.add_header('Content-Length', len(jsondataasbytes))
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
        data['AnginaPectoris'] = request.form.get('AnginaPectoris')
        data['Vessels'] = request.form.get('Vessels')
        data['Chest_Pain_Type'] = request.form.get('ChestPainType')
        data['Sugar_level'] = request.form.get('Sugarlevel')
        data['Electrocardiographic'] = request.form.get('Electrocardiographic')
        data['Slope'] = request.form.get('Slope')
        data['Thal_Rate'] = request.form.get('ThalRate')
        data['Age'] = request.form.get('Age')
        data['Pressure'] = request.form.get('Pressure')
        data['Cholesterol'] = request.form.get('Cholesterol')
        data['MaxHeartRate'] = request.form.get('MaxHeartRate')
        data['OldPeak'] = request.form.get('OldPeak')

        try:
            response = str(get_prediction(data['Sex'],
                                          data['AnginaPectoris'],
                                          data['Vessels'],
                                          data['Chest_Pain_Type'],
                                          data['Sugar_level'],
                                          data['Electrocardiographic'],
                                          data['Slope'],
                                          data['Thal_Rate'],
                                          data['Age'],
                                          data['Pressure'],
                                          data['Cholesterol'],
                                          data['MaxHeartRate'],
                                          data['OldPeak']))
            print(response)
        except ConnectionError:
            response = json.dumps({"error": "ConnectionError"})
        return redirect(url_for('predicted', response=response))
    return render_template('form.html', form=form)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8181, debug=True)
