import json

def readFile_to_jsonDict(filename):
    jsonfo = open(filename, "r")
    data = json.load(jsonfo)

    jsonfo.close()
    return data


def jsonDict_to_eagleDict(jsonDict, filePath, maxFile=0):
    data = jsonDict
    #print(data['info']['illust']['title'])

    pageUrl = data['info']['illust']['url']
    tags = data['info']['illust']['tags']

    # TODO: filePath拿到的是描述txt檔，仍需要透過txtDict拿到的path.ext改寫副檔名，才會拿到圖片本體
    pathExt = data['info']['path'][0]['src'].split('.')[-1]

    folderData = {}

    baseData = {
        "name": data['info']['illust']['title'],
        "annotation": data['info']['illust']['caption'],
        "website": pageUrl,
        "tags": list(tags),
        "modificationTime":  data['info']['illust']['posted']
    }

    maxFile = int(maxFile)
    if maxFile > 0:
        basePath = filePath.rsplit('/', 1)[0]
        items = []
        for itemNum in range(1,maxFile+1):
            items.append({"path": (basePath+"/"+"%d" % (itemNum))+'.'+pathExt} | baseData)
            items.append({"path": (basePath+"/"+"%02d" % (itemNum))+'.'+pathExt} | baseData)
            pass
        data = {"items": items} | folderData
        pass
    else:
        baseFilePath = filePath.rsplit('.', 1)[0]
        singleItemData = {"path": baseFilePath+'.'+pathExt} | baseData
        data = singleItemData | folderData
        pass

    return data

def jsonDict_to_puserId(jsonDict):
    return jsonDict['info']['member']['id']
def jsonDict_to_puserName(jsonDict):
    return jsonDict['info']['member']['name']

if __name__ == "__main__":
    import sys

    try:
        filePath = sys.argv[1]
        maxFile = sys.argv[2]
        #print(sys.argv[1])
    except IndexError as e:
        filePath = "sample/(12532) 砂(s73d)/2017-07-29 (64114679) 魔理沙.json"

    jsonDict = readFile_to_jsonDict(filePath)
    reqData = jsonDict_to_eagleDict(jsonDict, filePath, maxFile)
    print(reqData)

    print("pixivId: "+jsonDict_to_puserId(jsonDict) + "  pixivName: "+ jsonDict_to_puserName(jsonDict))
