import txtDict_to_eagleDict
import jsonDict_to_eagleDict
import os


if __name__ == "__main__":
    import sys

    try:
        basePath = sys.argv[1]
    except IndexError as e:
        basePath = "./sample/"

    for root, dirs, files in os.walk(basePath, topdown=False):
        for fileName in files:
            # print(fileName)
            fileNameWithoutExt = fileName.split('.')[0]
            fileExt = fileName.split('.')[-1]
            baseFilePath = os.path.join(root)
            filePath = os.path.join(baseFilePath, fileName)

            # 若該檔案名稱是meta，代表這個資料夾是一個圖集
            maxNum = 0
            if fileNameWithoutExt == 'meta':
                # 計算圖片數量
                folderFileList = os.listdir(baseFilePath)
                nameList = list(map(lambda x: x.split('.')[0] ,folderFileList))
                nameList.sort(reverse=True)
                for theName in nameList:
                    try:
                        int(theName)
                        maxNum = int(theName)
                        break
                    except ValueError:
                        continue
                    else:
                        continue

            # 製作Eagle Request Body
            if fileExt == 'txt':
                txtDict = txtDict_to_eagleDict.readFile_to_txtDict(filePath)
                eagleData = txtDict_to_eagleDict.txtDict_to_eagleDict(txtDict, filePath, maxNum)
            elif fileExt == 'json':
                jsonDict = jsonDict_to_eagleDict.readFile_to_jsonDict(filePath)
                eagleData = jsonDict_to_eagleDict.jsonDict_to_eagleDict(jsonDict, filePath, maxNum)
            else:
                continue

            # 查詢Eagle資料夾id
            
            print(eagleData)

            

            # filePath = os.path.join(baseFilePath, fileName)
            # fileExt = fileName.split('.')[-1]

            # print(filePath)
            # print(os.path.join(root))
            # if fileExt == 'txt':
                # pass
                # txtDict = txtDict_to_eagleDict.readFile_to_txtDict(filePath)
                # print(txtDict)
                # eagleData = txtDict_to_eagleDict.txtDict_to_eagleDict(txtDict, filePath, 0)
                # print(eagleData)
            # print(filePath)
            # print(os.path.join(root, name))

        # for name in dirs:
        #     print(os.path.join(root, name))