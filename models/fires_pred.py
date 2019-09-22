import os
import json
from watson_developer_cloud import VisualRecognitionV3

visual_recognition = VisualRecognitionV3(
    '2018-03-19',
    iam_apikey='kHJrcO7-6xu6U8aY8sRU2WdLVQttkt4dUrY5JQivVyje')
def predict_drone(filename):
    PATH = os.getcwd() + '/assets/'+filename+'.jpg'
    print(PATH)
    with open(PATH, 'rb') as images_file:
        classes = visual_recognition.classify(
            images_file,
            threshold='0.6',
        classifier_ids='Firerecognition_1441757010').get_result()
    return json.dumps(classes, indent=2)