import sys
import os
import datetime
from operators.op import op
import re

DATATYPES = {
    str: "string",
    dict: "object",
    list: "array",
    int: "integer",
    float: "float",
    bool: "boolean",
    bytes: "bytes"
}


def generateNode(attribute, node, value, label="", description=""):
    tmpLabel = label
    titleLabel = label
    descriptionLabel = description
    if(description == "" or tmpLabel == ""):
        tmpLabel = generateLabelFromName(attribute)
        titleLabel = tmpLabel.title()
        descriptionLabel = tmpLabel.capitalize()
    return createNodes(parent=node, data=value, attr=attribute,
                        label=titleLabel, description=descriptionLabel)
    

def createNodes(parent, attr, data, label, description, ref=None, tmpType=None):

    node = createNode(parent=parent, attr=attr, data=data,
                      label=label, ref=ref, description=label)

    if (node["type"]["datatype"] == "object"):
        tmpData = {}
        for attribute in data:
            value = data[attribute]
            tmpData[attribute] = generateNode(attribute, node, value)

        node["data"] = tmpData
    elif(node["type"]["datatype"] == "array"):
        tmpData = {}
        for attribute, value in enumerate(data):
            stringIndex = str(attribute)
            tmpData[stringIndex] = generateNode(stringIndex, node, value, stringIndex, stringIndex)

        node["data"] = tmpData

    return node


def createNode(parent, attr, data, label, description, ref=None, tmpType=None):
    global BPN
    if (attr == None):
        return None

    if (tmpType == None):
        tmpType = {"unit": None, "datatype": "object"}
        
    if (data!=None and type(data) not in DATATYPES):
        print(f"Invalid data type! in data [{data}]")
        return None

    datatype = "undefined"
    if(data != None):
        datatype = DATATYPES[type(data)]

    tmpType["datatype"] = datatype

    if ref != None:
        reference = ref
    elif parent["ref"] == "/":
        reference = "/" + attr
    else:
        reference =  "/".join([parent["ref"], attr])

    return {
        "id": attr,
        "label": label,
        "description": description,
        "type": tmpType,
        "ref": reference,
        "audit": {
            "created": op.timestamp(),
            "createdBy": BPN,
            "updated": op.timestamp(),
            "updatedBy": BPN,
        },
        "data": data
    }


def generateDataModel(filepath):
    global BPN
    # Load file content
    initialData = op.readJsonFile(filepath)

    dataModel = createNodes(parent={}, attr="passport", data=initialData, label="Digital Product Passport",
                            description="Root passport node", ref="/")

    op.toJsonFile(sourceObject=dataModel,
                  jsonFilePath="output/jsonData-"+str(op.timestamp())+".json")


def generateLabelFromName(name):
    return " ".join(re.findall('[aA-zZ][^A-Z]*', name))


if __name__ == '__main__':
    FILE_PATH = "../dataModel.json"
    BPN = "user1"
    paramsLen = len(sys.argv)
    if paramsLen > 1:
        FILE_PATH = sys.argv[1]
    if paramsLen > 2:
        BPN = sys.argv[2]

    generateDataModel(FILE_PATH)
