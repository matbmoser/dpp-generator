import sys
import os
import datetime
from operators.op import op
import re
import copy

DATATYPES = {
    str: "string",
    dict: "object",
    list: "array",
    int: "integer",
    float: "float",
    bool: "boolean",
    bytes: "bytes"
}


def generateNode(attribute, node, value, label="", description="", unit=None):
    tmpLabel = label
    titleLabel = label
    descriptionLabel = description
    if(description == "" or tmpLabel == ""):
        tmpLabel = generateLabelFromName(attribute)
        titleLabel = tmpLabel.title()
        descriptionLabel = tmpLabel.capitalize()
    return createNodes(parent=node, data=value, attr=attribute,
                        label=titleLabel, description=descriptionLabel, unit=unit)
    

def createNodes(parent, attr, data, label, description, ref=None, tmpType=None, unit=None):
    node = createNode(parent=parent, attr=attr, data=data,
                      label=label, ref=ref, description=label, unit=unit)

    if (node["type"]["dataType"] == "object"):
        tmpData = list()
        if("unit" in data and "value" in data):
            unitValue = copy.deepcopy(data["unit"])
            valueUnit = copy.deepcopy(data["value"])
            del data["unit"]
            del data["value"]
            tmpData.append(generateValueNode(parent=parent, unit=unitValue, value=valueUnit, ref=ref))
        
        for attribute, value in data.items():
            tmpData.append(generateNode(attribute, node, value, unit))

        node["children"] = tmpData
        
    elif(node["type"]["dataType"] == "array"):
        tmpData = list()
        for attribute, value in enumerate(data):
            tmpData.append(generateNode(attribute, node, value, attribute, attribute, unit))

        node["children"] = tmpData

    return node

def generateValueNode(parent, unit=None, value=None, ref=None, tmpType=None):
    global BPN

    attr = "value"
    if (tmpType == None):
        tmpType = {"typeUnit": unit, "dataType": "object"}
        
    if (value!=None and type(value) not in DATATYPES):
        print(f"Invalid data type! in data [{value}]")
        return None

    datatype = "undefined"
    if(value != None):
        datatype = DATATYPES[type(value)]

    tmpType["dataType"] = datatype

    if ref != None:
        reference = ref
    elif parent["ref"] == ".":
        reference = attr
    elif isinstance(attr, int):
        reference =  parent["ref"] + "["+str(attr)+"]"
    else:
        reference =  ".".join([parent["ref"], attr])

    return {
        "id": attr,
        "label": attr,
        "description": attr,
        "type": tmpType,
        "ref": reference,
        "children": [],
        "data": value
    }


def createNode(parent, attr, data, label, description, ref=None, tmpType=None, unit=None):
    global BPN
    if (attr == None):
        return None

    if (tmpType == None):
        tmpType = {"typeUnit": unit, "dataType": "object"}
        
    if (data!=None and type(data) not in DATATYPES):
        print(f"Invalid data type! in data [{data}]")
        return None

    datatype = "undefined"
    if(data != None):
        datatype = DATATYPES[type(data)]

    tmpType["dataType"] = datatype

    if ref != None:
        reference = ref
    elif parent["ref"] == ".":
        reference = attr
    elif isinstance(attr, int):
        reference =  parent["ref"] + "["+str(attr)+"]"
    else:
        reference =  ".".join([parent["ref"], attr])

    if(not tmpType["dataType"] in ["array", "object"]):
        return {
            "id": attr,
            "label": label,
            "description": description,
            "type": tmpType,
            "ref": reference,
            "children": [],
            "data": data
        }
    return {
        "id": attr,
        "label": label,
        "description": description,
        "type": tmpType,
        "ref": reference,
        "children": [],
        "data": None
    }

def generateDataModel(filepath):
    global BPN
    # Load file content
    initialData = op.readJsonFile(filepath)

    dataModel = createNodes(parent={}, attr="passport", data=initialData, label="Digital Product Passport",
                            description="Root passport node", ref=".")

    op.toJsonFile(sourceObject=dataModel,
                  jsonFilePath="output/jsonData-"+str(op.timestamp())+".json")


def generateLabelFromName(name):
    return " ".join(re.findall('[aA-zZ][^A-Z]*', name))


if __name__ == '__main__':
    FILE_PATH = "./dataModel.json"
    BPN = "user1"
    paramsLen = len(sys.argv)
    if paramsLen > 1:
        FILE_PATH = sys.argv[1]
    if paramsLen > 2:
        BPN = sys.argv[2]

    generateDataModel(FILE_PATH)
