import pickle
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
import os
import time
import numpy as np
import pandas as pd
import glob
import requests
# def stream_handler(message):
#     print("")
#     # print(message["event"]) # put
#     # print(message["path"]) # /-K7yGTTEp7O549EzTYtI
#     # print(message["data"]) # {'title': 'Pyrebase', "body": "etc..."}
#     # redirect(check_result)
#
# my_stream = database.stream(stream_handler)

# def extract_data(s):
#     s = s[1:]
#     s = s[:-1]
#     # no more []
#     l = s.split(',')
#     l = [float(i) for i in l]
#     print(l)
#     print(type(l))
#     return l




@csrf_exempt
def check_result(request):

    # data = database.get().val()
    # res = predict(data)

    return JsonResponse(res, safe=False)


@csrf_exempt
def index(request):
    return render(request, 'index.html' , {'text' : "test"})
