import json

from flask import Flask, render_template, jsonify, url_for, request
from pyfcm import FCMNotification

from models.istherefire import predict_fire, confidence_fire
from models.fires_pred import predict_drone
app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('index.html', my_string="Hello, world!")

@app.route("/predict", methods = ['POST'])
def predict():
    val = predict_fire(20, 20, 6, 0)
    if val == 1:
        conf = confidence_fire(20, 20, 6, 0)
        result = {
            "val": int(val)
        }
        print(result)
    return jsonify(result)

@app.route("/send_notification", methods = ["POST"])
def notifcation(message_body=None):
    push_service = FCMNotification(api_key="AAAAU7_ST5A:APA91bHC8Xz7wYSJJW_OoWNmc5d3m90lmsiWjBLwP2VUT1mgXM4d9sbTJ9tAKEMJVAeYgzj3OQ1STQ7oP-4lQKHLC1VR0kRWLh9oQJRO_qWIHjErMofksn1cQ5IqjfVGDJUHq1RSVqPE")
    registration_id = "eBdaqLiakOY:APA91bEGqGVWEhlapxasPSj-vC0mRbDSc9FL64043SaowLRDlE6sa9nRUOf1BVQ_2hkOUa9WD5FxXI1j23dvBVfuLk18CZFPGN3Va_1slmg5ccyHJoTPGG0JEY7XigcJA1htDQYZeRP2"
    message_title = "Fire alert!"
    message_body = "Forest fire reported nearby!"
    result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)
    return jsonify({"status": "ok"})

@app.route("/predict_drone")
def predict_drone_api():
    return render_template('predict.html')

@app.route("/id_forest", methods=["POST"])
def id_forest():
    print(request.json)
    req = request.json
    res = predict_drone(req["filename"])
    res_load = json.loads(res)
    print(type(res_load))
    return_obj = res_load['images'][0]['classifiers'][0]['classes'][0]
    return jsonify(return_obj)

# ideally this should have been merged with /send_notification
@app.route("/notify", methods = ["POST"])
def notify():
    push_service = FCMNotification(api_key="AAAAU7_ST5A:APA91bHC8Xz7wYSJJW_OoWNmc5d3m90lmsiWjBLwP2VUT1mgXM4d9sbTJ9tAKEMJVAeYgzj3OQ1STQ7oP-4lQKHLC1VR0kRWLh9oQJRO_qWIHjErMofksn1cQ5IqjfVGDJUHq1RSVqPE")
    registration_id = "eBdaqLiakOY:APA91bEGqGVWEhlapxasPSj-vC0mRbDSc9FL64043SaowLRDlE6sa9nRUOf1BVQ_2hkOUa9WD5FxXI1j23dvBVfuLk18CZFPGN3Va_1slmg5ccyHJoTPGG0JEY7XigcJA1htDQYZeRP2"
    message_title = "Fire confirmed!"
    message_body = "Please evacuate immediately!"
    result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)
    return jsonify({"status": "ok"})

@app.route("/location", methods = ["POST"])
def location():
    print(request.json)
    return jsonify({"status": "ok"})

if __name__ == '__main__':
   app.run(debug=True, host="0.0.0.0", port=5000)