# Routes for the Version 1 API
from scrape import (
    myuttyler_authenticate, student_center, account_summary, todo_list, 
    get_schedule, blackboard_authenticate, get_announcements,
    get_myutt_info, get_grades
)
from formencode.variabledecode import variable_encode
from flask import Flask, request, jsonify, Blueprint
import time
import os
import traceback
import json
v1 = Blueprint('v1', __name__, url_prefix="/1.0")

GENERIC_ERROR = "serverError"

######################################################################### 
# Helpers
######################################################################### 
def my_jsonify(myDict):
    ''' 
    Return a flask Response object without newlines in the JSON. I don't know
    why I care so much, but apparently I do.
    '''
    response = jsonify(myDict)

    newlineJSON = response.response[0]
    noNewlineJSON = json.dumps(json.loads(newlineJSON))
    response.response[0] = noNewlineJSON

    return response

def err_json(myerrStr, status_code = 500):
    response = my_jsonify({"error": myerrStr})
    response.status_code = status_code
    return response

######################################################################### 
# Routes
######################################################################### 
@v1.route('/grades', methods=["POST"])
def grades():
    dataDict = variable_encode(request.form)
    try:
        username = dataDict.get('username')
        password = dataDict.get('password')
        cookie = blackboard_authenticate(username, password)
        if not cookie:
            return err_json("authenticationFailure", 401)

        data = get_grades(cookie)

        # Wrap in a dict to preserve order of grades
        return my_jsonify({"grades":data})
    except Exception, e:
        return err_json(GENERIC_ERROR)

@v1.route('/announcements', methods=["POST"])
def announcements():
    dataDict = variable_encode(request.form)
    try:
        username = dataDict.get('username')
        password = dataDict.get('password')
        cookie = blackboard_authenticate(username, password)
        if not cookie:
            return err_json("authenticationFailure", 401)

        data = get_announcements(cookie)

        # Wrap in a dict since jsonify doesn't accept pure lists
        return my_jsonify({"announcements":data})

    except Exception, e:
        return err_json(GENERIC_ERROR)

@v1.route('/myuttyler', methods=["POST"])
def myuttyler():
    dataDict = variable_encode(request.form)
    try:
        username = dataDict.get('username')
        password = dataDict.get('password')
        cookie = myuttyler_authenticate(username, password)
        if not cookie:
            return err_json("authenticationFailure", 401)

        data = get_myutt_info(cookie)

        # Wrap in a dict since jsonify doesn't accept pure lists
        return my_jsonify({"myuttyler":data})

    except Exception, e:
        return err_json(GENERIC_ERROR)

