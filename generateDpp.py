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


def createNodes(parent, attr, data, label, description, ref=None, roles=[], tmpType=None):

    node = createNode(parent=parent, attr=attr, data=data,
                      label=label, ref=ref, description=label, roles=[])

    if (node["type"]["datatype"] != "object"):
        return node

    tmpData = {}
    for attribute in data:
        value = data[attribute]
        tmpLabel = generateLabelFromName(attribute)
        tmpNode = createNodes(parent=node, data=value, attr=attribute,
                              label=tmpLabel.title(), description=tmpLabel.capitalize())
        tmpData[attribute] = tmpNode

    node["data"] = tmpData
    return node


def createNode(parent, attr, data, label, description, ref=None, roles=[], tmpType=None):
    global BPN
    if (attr == None):
        return None

    if (tmpType == None):
        tmpType = {"unit": None, "datatype": "object"}

    if (type(data) not in DATATYPES):
        print(f"Invalid data type! in data [{data}]")
        return None

    tmpType["datatype"] = DATATYPES[type(data)]

    return {
        "key": attr,
        "label": label,
        "description": description,
        "type": tmpType,
        "ref": ref if ref != None else str(os.path.join("/", parent["ref"], attr)),
        "audit": {
            "created": op.timestamp(),
            "createdBy": BPN,
            "updated": op.timestamp(),
            "updatedBy": BPN,
        },
        "roles": roles,
        "data": data
    }


def generateDataModel(filepath):
    global BPN
    # Load file content
    initialData = op.readJsonFile(filepath)

    dataModel = createNodes(parent={}, attr="passport", data=initialData, label="Digital Product Passport",
                            description="Root passport node", ref="/", roles=["oem", "recycler", "dismantler"])

    op.toJsonFile(sourceObject=dataModel,
                  jsonFilePath="output/jsonData-"+str(op.timestamp())+".json")


def generateLabelFromName(name):
    return " ".join(re.findall('[aA-zZ][^A-Z]*', name))


if __name__ == '__main__':
    FILE_PATH = "../dataModel.json"
    BPN = "BPN_21561231_892151"
    paramsLen = len(sys.argv)
    if paramsLen > 1:
        FILE_PATH = sys.argv[1]
    if paramsLen > 2:
        BPN = sys.argv[2]

    generateDataModel(FILE_PATH)
