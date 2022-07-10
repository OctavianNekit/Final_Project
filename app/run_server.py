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


modelpath = "/app/app/models/GB_pipeline.dill"
load_model(modelpath)


@app.route("/", methods=["GET"])
def general():
    return """Welcome to the stroke prediction website,  Please use 'http://<address>/predict' to POST"""


@app.route("/predict", methods=["POST"])
def predict():
    data = {"success": False}
    dt = strftime("[%Y-%b-%d %H:%M:%S]")
    if flask.request.method == "POST":

        Sex, ChestPainType, RestingECG, ExerciseAngina, ST_Slope, Age, RestingBP, Cholesterol, FastingBS, MaxHR, Oldpeak \
            = '', '', '', '', '', '', '', '', '', '', ''

        request_json = flask.request.get_json()

        if request_json["Sex"]:
            Sex = request_json['Sex']

        if request_json["ChestPainType"]:
            ChestPainType = request_json['ChestPainType']

        if request_json["RestingECG"]:
            RestingECG = request_json['RestingECG']

        if request_json["ExerciseAngina"]:
            ExerciseAngina = request_json['ExerciseAngina']

        if request_json["ST_Slope"]:
            ST_Slope = request_json['ST_Slope']

        if request_json["Age"]:
            Age = request_json['Age']

        if request_json["RestingBP"]:
            RestingBP = request_json['RestingBP']

        if request_json["Cholesterol"]:
            Cholesterol = request_json['Cholesterol']

        if request_json["FastingBS"]:
            FastingBS = request_json['FastingBS']

        if request_json["MaxHR"]:
            MaxHR = request_json['MaxHR']

        if request_json["Oldpeak"]:
            Oldpeak = request_json['Oldpeak']

        logger.info(f'{dt} Data: Sex={Sex}, '
                    f'ChestPainType={ChestPainType}, '
                    f'RestingECG={RestingECG}',
                    f'ExerciseAngina={ExerciseAngina}',
                    f'ST_Slope={ST_Slope}',
                    f'Age={Age}',
                    f'RestingBP={RestingBP}',
                    f'Cholesterol={Cholesterol}',
                    f'FastingBS={FastingBS}',
                    f'MaxHR={MaxHR}',
                    f'Oldpeak={Oldpeak}')
        try:
            preds = model.predict_proba(pd.DataFrame({"Sex": [Sex],
                                                      "ChestPainType": [ChestPainType],
                                                      "RestingECG": [RestingECG],
                                                      "ExerciseAngina": [ExerciseAngina],
                                                      "ST_Slope": [ST_Slope],
                                                      "Age": [Age],
                                                      "RestingBP": [RestingBP],
                                                      "Cholesterol": [Cholesterol],
                                                      "FastingBS": [FastingBS],
                                                      "MaxHR": [MaxHR],
                                                      "Oldpeak": [Oldpeak]}))
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
