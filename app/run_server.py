import logging
import os
from logging.handlers import RotatingFileHandler
from time import strftime
import dill
import flask
import pandas as pd

dill._dill._reverse_typemap['ClassType'] = type

app = flask.Flask(__name__)
model = None

handler = RotatingFileHandler(filename='app.log', maxBytes=100000, backupCount=10)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)


def load_model(model_path):
    global model
    with open(model_path, 'rb') as f:
        model = dill.load(f)
    print(model)


modelpath = "app/app/models/GB_pipeline.dill"
load_model(modelpath)


@app.route("/", methods=["GET"])
def general():
    return """Welcome to the stroke prediction website,  Please use 'http://<address>/predict' to POST"""


@app.route("/predict", methods=["POST"])
def predict():
    data = {"success": False}
    dt = strftime("[%Y-%b-%d %H:%M:%S]")
    if flask.request.method == "POST":

        Sex, AnginaPectoris, Vessels, ChestPainType, SugarLevel, Electrocardiographic, Slope, ThalRate,\
        Age, Pressure, Cholesterol, MaxHeartRate, OldPeak = '', '', '', '', '', '', '', '', '', '', '', '', ''

        request_json = flask.request.get_json()

        if request_json["Sex"]:
            Sex = request_json['Sex']

        if request_json["AnginaPectoris"]:
            AnginaPectoris = request_json['AnginaPectoris']

        if request_json["Vessels"]:
            Vessels = request_json['Vessels']

        if request_json["ChestPainType"]:
            ChestPainType = request_json['ChestPainType']

        if request_json["SugarLevel"]:
            SugarLevel = request_json['SugarLevel']

        if request_json["Electrocardiographic"]:
            Electrocardiographic = request_json['Electrocardiographic']

        if request_json["Slope"]:
            Slope = request_json['Slope']

        if request_json["ThalRate"]:
            ThalRate = request_json['ThalRate']

        if request_json["Age"]:
            Age = request_json['Age']

        if request_json["Pressure"]:
            Pressure = request_json['Pressure']

        if request_json["Cholesterol"]:
            Cholesterol = request_json['Cholesterol']

        if request_json["MaxHeartRate"]:
            MaxHeartRate = request_json['MaxHeartRate']

        if request_json["OldPeak"]:
            OldPeak = request_json['OldPeak']

        logger.info(f'{dt} Data: Sex={Sex}, '
                    f'AnginaPectoris={AnginaPectoris}, '
                    f'Vessels={Vessels}',
                    f'ChestPainType={ChestPainType}',
                    f'SugarLevel={SugarLevel}',
                    f'Electrocardiographic={Electrocardiographic}',
                    f'Slope={Slope}',
                    f'ThalRate={ThalRate}',
                    f'Age={Age}',
                    f'Pressure={Pressure}',
                    f'Cholesterol={Cholesterol}',
                    f'MaxHeartRate={MaxHeartRate}',
                    f'OldPeak={OldPeak}')
        try:

            preds = model.predict_proba(pd.DataFrame({"Sex": [Sex],
                                                      "AnginaPectoris": [AnginaPectoris],
                                                      "Vessels": [Vessels],
                                                      "ChestPainType": [ChestPainType],
                                                      "SugarLevel": [SugarLevel],
                                                      "Electrocardiographic": [Electrocardiographic],
                                                      "Slope": [Slope],
                                                      "ThalRate": [ThalRate],
                                                      "Age": [Age],
                                                      "Pressure": [Pressure],
                                                      "Cholesterol": [Cholesterol],
                                                      "MaxHeartRate": [MaxHeartRate],
                                                      "OldPeak": [OldPeak]}))

        except AttributeError as e:
            logger.warning(f'{dt} Exception: {str(e)}')
            data['predictions'] = str(e)
            data['success'] = False
            return flask.jsonify(data)

        data["predictions"] = preds[:, 1][0]
        # indicate that the request was a success
        data["success"] = True

    # return the data dictionary as a JSON response
    return flask.jsonify(data)


# if this is the main thread of execution first load the model and
# then start the server
if __name__ == "__main__":
    print(("* Loading the model and Flask starting server..."
           "please wait until server has fully started"))
    port = int(os.environ.get('PORT', 8180))
    app.run(host='0.0.0.0', debug=True, port=port)
