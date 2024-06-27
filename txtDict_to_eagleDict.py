from datetime import datetime

def readFile_to_txtDict(filename):
    txt_fo = open(filename, "r")

    #for line in txt_fo.readlines():
    #    line = line.strip()
    #    print('1:'+line)

    #for index, line in enumerate(txt_fo):
    #    line = line.strip()
    #    print(str(index)+': '+line)

    #print "读取的数据为: %s" % (line)

    data = {}

    while True:
        line1 = txt_fo.readline()
        line2 = txt_fo.readline()
        if not line2: break  # EOF
        #print('line1: '+line1+'line2: '+line2)

        key = line1.strip()
        value = line2.strip()

        data[key] = value

    # 关闭文件
    txt_fo.close()
    return data

def txtDict_to_eagleDict(txtDict, filePath, maxFile=0):
    data = txtDict
    pageUrl = data.get('illust.pageUrl') if data.get('illust.pageUrl') is not None else data.get('path.mangaIndexPage')
    tags = {k: v for k, v in data.items() if any(x in k for x in ['illust.tags'])}.values()
    pathExt = data.get("path.ext")

    illustYear = data.get("illust.dateTime.year")
    illustMonth = data.get("illust.dateTime.month")
    illustDay = data.get("illust.dateTime.day")
    illustHour = data.get("illust.dateTime.hour")
    illustMinute = data.get("illust.dateTime.minute")
    illustTs = int(datetime(2008, 10, 21, 10,53).timestamp()) * 100

    folderData = {}

    baseData = {
        "name": data.get("illust.title"),
        "annotation": data.get("illust.comment"),
        "website": pageUrl,
        "tags": list(tags),
        "modificationTime": illustTs
    }

    maxFile = int(maxFile)
    if maxFile > 0:
        basePath = filePath.rsplit('/', 1)[0]
        items = []
        for itemNum in range(1,maxFile+1):
            items.append({"path": (basePath+"/"+"%02d" % (itemNum))+pathExt} | baseData)
            pass
        data = {"items": items} | folderData
        pass
    else:
        baseFilePath = filePath.rsplit('.', 1)[0]
        singleItemData = {"path": baseFilePath+''+pathExt } | baseData
        data = singleItemData | folderData
        pass

    return data

def txtDict_to_puserId(txtDict):
    return txtDict.get('member.id')
def txtDict_to_puserName(txtDict):
    return txtDict.get('member.name')

if __name__ == "__main__":
    import sys
    #fib(int(sys.argv[1]))

    try:
        filePath = sys.argv[1]
        maxFile = sys.argv[2]
        #print(sys.argv[1])
    except IndexError as e:
        filePath = "sample/つのじゅ - ___ (27116379).txt"

    txtDict = readFile_to_txtDict(filePath)
    #print(txtDict)
    reqData = txtDict_to_eagleDict(txtDict, filePath, maxFile)
    print(reqData)
    print("pixivId: "+txtDict_to_puserId(txtDict) + "  pixivName: "+ txtDict_to_puserName(txtDict))

