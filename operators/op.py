# Set log levels
from shutil import copyfile, move
import shutil
from os.path import isfile, join
from os import listdir
import os
import sys
import json

LOGLEVELS = {"NONE": 0, "CRITICAL": 1, "EXCEPTION": 2,
             "ERROR": 3, "WARNING": 4, "INFO": 5, "STATS": 6, "DEBUG": 7}
LOGLEVEL = LOGLEVELS["STATS"]


from datetime import datetime, timezone

"""
Class that defines operations in files, directories, clases, etc...
"""
class op:
    @staticmethod
    def jsonStringToObject(jsonString):
        data = json.loads(jsonString)
        return data

    @staticmethod
    def toJson(sourceObject,indent=0,ensure_ascii=True):
        return json.dumps(obj=sourceObject,indent=indent,ensure_ascii=ensure_ascii)
    
    @staticmethod
    def toJsonFile(sourceObject,jsonFilePath,fileOpenMode="w",indent=2):
        tmpJsonString=op.toJson(sourceObject=sourceObject,indent=indent)
        op.writeToFile(data=tmpJsonString, filePath=jsonFilePath,openMode=fileOpenMode, end="")
        
    @staticmethod
    def readJsonFile(filePath,encoding="utf-8"):
        data=None
        f = open(filePath,"r",encoding=encoding)
        data = json.load(f)
        f.close()
        
        return data  
      
    @staticmethod
    def timestamp(zone=timezone.utc, string=False):
        timestamp = datetime.timestamp(datetime.now(zone))
        if (string):
            return str(timestamp)
        
        return timestamp
    
    @staticmethod
    def getDatetime(zone=timezone.utc, string=False):
        date = datetime.now(zone)
        if (string):
            return str(date)
        
        return date
    
    @staticmethod
    def startLog(logFile=None):
        if(logFile == None):
            logFile = f"./log/generator-{op.timestamp()}.log"
        openMessage = "Starting Server Log Messages..."
        op.writeToFile(data=openMessage, filePath=logFile,
                       openMode="w+", end="\n")

    @staticmethod
    def valueEmpty(obj):
        return "" if obj == None or obj == "" else obj

    # Method to set value none by default
    @staticmethod
    def valueNone(obj):
        return None if obj == None or obj == "" else obj

    # Print log Operation
    @staticmethod
    def printLog(messageStr, logType="DEBUG", e=None):
        global LOGLEVEL, LOGLEVELS, LOGFILE
        if(LOGFILE == None):
            op.startLog()
        # If the log level requested is lower than the actual log level
        if LOGLEVEL < LOGLEVELS[logType]:
            return None

        # Add the log description and exception if not empty
        logInfo = "["+logType+"]:"
        if(e != None):
            logInfo += "[" + str(e) + "]."

        # Print the log
        logData = " ".join([logInfo, messageStr])
        op.writeToFile(data=logData, filePath=LOGFILE, openMode="a+", end="\n")
        return print(logData)

    # Init dinamically the new class
    @ staticmethod
    def createClass(newClass, *args, **kwargs):
        # Get slices
        slices = newClass.split('.')

        # Count the number of slices
        lenSlices = len(slices)

        # Check if the number of slices
        if lenSlices == 1:
            slices.append(slices[0])

        # Import Class
        importedClass = __import__(".".join(slices[:-1]))

        # For every component add attributes
        for component in slices[1:]:
            importedClass = getattr(importedClass, component)

        # Create the class
        return importedClass(*args, **kwargs)

    @ staticmethod
    def pathExists(pathName):
        pathFile = os.path.exists(pathName)
        return pathFile

    @ staticmethod
    def makeDir(nameDir, permits=0o777):
        if op.pathExists(nameDir):
            return True
        os.makedirs(nameDir, permits)
        return True
    
    @ staticmethod
    def deleteDir(nameDir):
        if not op.pathExists(nameDir):
            return False
        
        shutil.rmtree(nameDir)
    @ staticmethod
    def copyFile(src, dst):
        return copyfile(src, dst)

    @ staticmethod
    def moveFile(src, dst):
        return move(src, dst)

    @ staticmethod
    def toString(inputFile, openmode="r", encoding=sys.stdout.encoding):
        str = open(inputFile, openmode, encoding=encoding).read()
        return str

    @ staticmethod
    def deleteFile(filePath):
        if not op.pathExists(filePath):
            return None

        os.remove(filePath)
        return True

    @ staticmethod
    def getPathWithoutFile(filePath):
        return os.path.dirname(filePath)

    @ staticmethod
    def writeToFile(data, filePath, openMode="r", end=""):
        if(data == "" or data == None):
            return None

        data = data + end
        path = op.getPathWithoutFile(filePath)

        if path == None or not op.pathExists(path):
            op.makeDir(path)

        file = open(filePath,
                    openMode, encoding=sys.stdout.encoding)
        file.write(data)
        file.close()
        return True
