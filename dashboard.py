import datetime
import json

def archiveListJSON(archiveList):
    jsonDict = {
        'archiveList': []
    }
    for archive in archiveList:
        jsonDict['archiveList'].append({
            'archiveName': archive.archiveName,
            'creationTime': archive.creationTime,
            'lastUpdateTime': archive.lastUpdateTime,
            'typeOfArchive': archive.typeOfArchive
        })

    return json.dumps(jsonDict, indent=4, sort_keys=True, default=str)
