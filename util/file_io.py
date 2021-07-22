import json
import datetime
import time
import os

#overwrites all data currently in the file
def writeToFile(path, data):
    with open(path, 'w') as fp:
        fp.write(data)

#reads and returns all data in fileName at path
def readFile(path):
    return open(path, 'r')

#writes data to txt file fileName at path
def appendToFile(path, data):
    with open(path, 'a') as fp:
        fp.write('\n' + data)

# returns an array with all filenames at path
def listFiles(path):
    return os.listdir(path)

# returns true if filename is a file in folder at path, false if not
def fileExistsIn(path, filename):
    allFiles = listFiles(path)
    if filename in allFiles: return True
    return False

#fetch json file at path
def fetchJSON(path):
    f = open(path, 'r')
    data = json.load(f)
    return data

#overwrites a json file at path with data
def writeJSON(path, data):
    json_obj = json.dumps(data, indent=4)
    with open(path, 'w') as fp:
        fp.write(json_obj)

#get current timestamp
def getTimestamp():
    today = datetime.date.today()
    date = today.strftime("%m/%d/%Y")
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    return date + " " + current_time