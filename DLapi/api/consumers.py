from channels.generic.websocket import WebsocketConsumer
import firebase_admin
import json
from random import randint
from time import sleep
import pickle
import pyrebase
import numpy as np
from .firebaseConfig import *
from api.models import Alert
from datetime import datetime
from tensorflow import keras


name_mapping_har = {'Downstairs': 0,
                'Jogging': 1,
                'Sitting': 2,
                'Standing': 3,
                'Upstairs': 4,
                'Walking': 5}

name_mapping_ecg = {'normal': 0,
                'Unknown Beats': 4,
                'Ventricular ectopic beats': 2,
                'Supraventricular ectopic beats': 1,
                'Fusion Beats': 3 }


loaded_model_har = keras.models.load_model('api/lstm-wisdmacc87.h5')
loaded_model_ecg = keras.models.load_model('api/ecgmodel.h5')
config = {
  "apiKey": "AIzaSyCkFcyC5DUUzoc7Lcq9i81c25dAuCnvLyI",
  "authDomain": "esante-20dd5.firebaseapp.com",
  "databaseURL": "https://esante-20dd5-default-rtdb.firebaseio.com",
  "projectId": "esante-20dd5",
  "storageBucket": "esante-20dd5.appspot.com",
  "messagingSenderId": "115623607398",
  "appId": "1:115623607398:web:879d52ddd819acf83441a7"
}

firebase = pyrebase.initialize_app(config)

database = firebase.database()
def predict_har(data):
    result_dict= {}
    for i in data.each()[-1:]:

        # array = np.array(list(i.values())[:-1])
        array = np.array(i.val())
        array = array.reshape(1, 200, 3)
        result = loaded_model_har.predict(array)
        result = result.argmax(axis=-1)
        print('\n' ,result)
        label = ""
        for key, value in name_mapping_har.items():
            if value == result[0]:
                label = key

        result_dict[i] = label


    return result_dict


def create_alert(_doctor=None, _priority=None, _user=None, _createdTime=None, _responseTime=None, _content=None,
                     _response=None):
        doc_ref = db.collection('alerts').document()
        alert = Alert(_id=doc_ref.id, _priority=_priority, _doctor=_doctor, _user=_user, _createdTime=_createdTime,
                      _responseTime=_responseTime, _content=_content, _response=_response)
        doc_ref.set(alert.todict())
        return alert





def predict_ecg(data):
    result_dict = {}
    for i in data.each()[-1:]:
        array = np.array(i.val())
        array = array.reshape(1,187)
        result = loaded_model_ecg.predict(array)
        result = result.argmax(axis=-1)
        print('\n', result)
        label = ""
        for key, value in name_mapping_ecg.items():
            if value == result[0]:
                label = key

        result_dict[i] = label

    return result_dict

hardata=[]
ecgdata = []
t=0

while 1 :
    if(hardata==[] or  hardata.val()!=database.child('HAR').get().val()):
        hardata = database.child('HAR').get()
        res = predict_har(hardata)
        activity=""
        for i in res.values() :
            if activity!=i:
                activity=i
                content="patient "+str(randint(1,10))+" is "+activity
                if(activity=="Jogging") :
                    priority="1"
                else:
                    priority="2"
                create_alert(_doctor=None , _createdTime=str(datetime.now().strftime("%H:%M:%S")) , _responseTime=None , _response=None , _priority=priority , _content=content , _user=None )
                sleep(1)
                # self.send(json.dumps({'message' : activity}))
    if ecgdata==[] or ecgdata.val() != database.child('ECG').get().val():
        ecgdata = database.child('ECG').get()
        print(database.child('ECG').get())
        sleep(1)
        res1 = predict_ecg(ecgdata)
        ecg_class = ""
        for i in res1.values():
            if i != "normal":
                ecg_class = i
                content = "patient " + str(randint(1, 10)) + " : arrhythmia type : " + ecg_class
                print("\n yo : " ,ecg_class)
                priority = "1"
                create_alert(_doctor=None , _createdTime=str(datetime.now().strftime("%H:%M:%S")) , _responseTime=None , _response=None , _priority=priority , _content=content , _user=None )
                sleep(1)






class WSConsumer(WebsocketConsumer) :
    def connect(self):
        self.accept()



