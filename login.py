from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json
from database import *
from dashboard import *
from fileSelect import *
from ocr import *
from flask_cors import CORS, logging
import time

if os.path.isdir('./temp') == False:
    os.mkdir('./temp')

# Thil file will handle all request (for GUI, DATA, MESSAGE) and flow of project
app = Flask(__name__, static_url_path='',
            static_folder='web/static', template_folder='web/templates')
CORS(app)


logingStatus = False
nextScan = True
currentUser = None
currentArchive = {
    'nameOfArchive': '',
    'typeOfArchive': '',
    'action': ''
}

# default redirect to login page
@app.route('/', methods=['GET', 'POST'])
def index():
    global logingStatus
    logingStatus = False
    return redirect(url_for('login'))

# testing flask is working or not
@app.route('/test', methods=['GET', 'POST'])
def test():
    return 'test'

# login page: to use application user need to login to the application
@app.route('/login', methods=['GET', 'POST'])
def login():
    global logingStatus
    global currentUser
    if request.method == 'POST':
        result = db.login(request.json['username'], request.json['password'])
        # print(request.json['username'], request.json['password'])
        if result == 'success':
            logingStatus = True
            currentUser = db.getUserObj(request.json['username'])
            return 'success'
        else:
            return result
    else:
        logingStatus = False
        return render_template('login.html')

# signin page: creating new account
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    global logingStatus
    logingStatus = False
    if request.method == 'POST':
        result = db.singin(
            request.json['username'],
            request.json['password'],
            request.json['firstname'],
            request.json['lastname'],
            request.json['email']
        )
        if result == 'success':
            return 'success'
        else:
            return result
    else:
        return render_template('signin.html')


# dashboard page: show all archive that user have created
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    global logingStatus
    if request.method == 'POST':
        return 'None'
    else:
        if logingStatus:
            return render_template('dashboard.html')
        else:
            return redirect(url_for('login'))

# send archive list for current user
@app.route('/dashboard/archivelist', methods=['GET'])
def getArchiveList():
    global logingStatus
    if logingStatus:
        if request.method == 'GET':
            archiveListDB = db.getArchiveList(currentUser)
            return jsonify(archiveListJSON(archiveListDB))

#  creating new archive
@app.route('/createArchive', methods=['GET'])
def createArchive():
    global logingStatus
    if logingStatus:
        if request.method == 'GET':
            return render_template('createArchive.html')

# ensure newly created archive have uniqe name
@app.route('/createArchive/create', methods=['GET'])
def create():
    global logingStatus
    if logingStatus:
        if request.method == 'GET':
            if db.isArchiveExist(request.args['name']):
                return 'ERROR: Name allrady taken'
            else:
                if request.args.get('selected') == 'simple':
                    global currentArchive
                    currentArchive['nameOfArchive'] = request.args.get('name')
                    currentArchive['typeOfArchive'] = 'simple'
                    currentArchive['action'] = 'save'
                    return 'success'
                else:
                    return 'invalid'

# create simple archive
@app.route('/createArchive/simple', methods=['GET'])
def simpleArchive():
    global logingStatus
    if logingStatus:
        if request.method == 'GET':
            global currentArchive
            return render_template('simpleArchive.html', name=currentArchive['nameOfArchive'])

# open file dialog select images(documents)
@app.route('/createArchive/simple/getList', methods=['GET'])
def getDocList():
    global logingStatus
    if logingStatus:
        if request.method == 'GET':
            responseData = {
                'docs': fm.selectFile()
            }
            return jsonify(json.dumps(responseData, indent=4, sort_keys=True, default=str))

# start scanning the image and sending back data as JSON
@app.route('/createArchive/simple/scan', methods=['GET'])
def scanDoc():
    global nextScan
    while nextScan == False:
        time.sleep(0.1)
    nextScan = False
    global logingStatus
    if logingStatus:
        if request.method == 'GET':
            path = request.args.get('img', '')

            ocr.cropImage(path)
            aadharRes = ocr.aadhar()
            if aadharRes != None:
                nextScan = True
                return jsonify(json.dumps(aadharRes, indent=4, sort_keys=True, default=str))

            docType = ocr.detect('./json/detect.json')
            res = None
            if docType == 'Driving Licence Of Indian Citizens':
                res = ocr.dataFind('./json/drive.json')
            elif docType == 'Dharmsinh Desai University ID Card':
                res = ocr.dataFind('./json/icard.json')
            elif docType == 'PAN Card Of Indian Citizens':
                res = ocr.dataFind('./json/pancard.json')
            elif docType == 'Standard 10th Marksheet Gujarat Board':
                res = ocr.dataFind('./json/std10.json')

            nextScan = True
            return jsonify(json.dumps(res, indent=4, sort_keys=True, default=str))

# saving archive in database
@app.route('/createArchive/save', methods=['POST'])
def saveDoc():
    global logingStatus
    if logingStatus:
        if request.method == 'POST':
            global currentArchive
            global currentUser
            db.createArchive(currentArchive['nameOfArchive'], datetime.datetime.now(), datetime.datetime.now(), currentArchive['typeOfArchive'], currentUser, json.dumps(request.json['data'], indent=4, sort_keys=True, default=str))
            return 'success'
# open archive from dashvoard
@app.route('/dashboard/open', methods=['GET'])
def openArchive():
    global logingStatus
    if logingStatus:
        if request.method == 'GET':
            global currentArchive
            currentArchive['nameOfArchive'] = request.args['archiveName']
            currentArchive['action'] = 'show'
            return 'success'
# show the selected archive
@app.route('/showArchive', methods=['GET'])
def showArchive():
    global logingStatus
    if logingStatus:
        if request.method == 'GET':
            return render_template('showArchive.html')
# get list of documenets that allready scanned
@app.route('/showArchive/get', methods=['GET'])
def showArchiveGet():
    global logingStatus
    if logingStatus:
        if request.method == 'GET':
            return db.getArchiveByName(currentArchive['nameOfArchive'])
# save modified archive
@app.route('/showArchive/save', methods=['POST'])
def showArchiveSave():
    global logingStatus
    if logingStatus:
        if request.method == 'POST':
            global currentArchive
            return db.saveArchive(currentArchive['nameOfArchive'], json.dumps(request.json['data'], indent=4, sort_keys=True, default=str))


if __name__ == '__main__':
    app.run()
