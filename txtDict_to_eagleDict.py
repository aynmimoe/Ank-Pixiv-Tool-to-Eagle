
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

def txtDict_to_eagleDict(txtDict, filePath, eagleFolderId, maxFile=0):
    data = txtDict
    pageUrl = data.get('illust.pageUrl') if data.get('illust.pageUrl') is not None else data.get('path.mangaIndexPage')
    tags = {k: v for k, v in data.items() if any(x in k for x in ['illust.tags'])}.values()

    # TODO: filePath拿到的是描述txt檔，仍需要透過txtDict拿到的path.ext改寫副檔名，才會拿到圖片本體
    pathExt = data.get("path.ext")

    folderData = {
        "folderId": eagleFolderId
    }

    maxFile = int(maxFile)
    if maxFile > 0:
        basePath = filePath.rsplit('/', 1)[0]
        items = []
        for itemNum in range(1,maxFile+1):
            items.append({
                "path": (basePath+"/"+"%02d" % (itemNum))+pathExt,
                "name": data.get("illust.title"),
                "annotation": data.get("illust.comment"),
                "website": pageUrl,
                "tags": list(tags),
            })
            pass
        data = {"items": items} | folderData
        pass
    else:
        baseFilePath = filePath.rsplit('.', 1)[0]
        singleItemData = {
            "path": baseFilePath+''+pathExt,
            "name": data.get("illust.title"),
            "annotation": data.get("illust.comment"),
            "website": pageUrl,
            "tags": list(tags),
        }
        data = singleItemData | folderData
        pass

    return data

if __name__ == "__main__":
    import sys
    #fib(int(sys.argv[1]))

    try:
        filePath = sys.argv[1]
        eagleFolderId = sys.argv[2]
        maxFile = sys.argv[3]
        #print(sys.argv[1])
    except IndexError as e:
        filePath = "sample/つのじゅ - ___ (27116379).txt"

    txtDict = readFile_to_txtDict(filePath)
    #print(txtDict)
    reqData = txtDict_to_eagleDict(txtDict, filePath, '0x00000', maxFile)
    print(reqData)

