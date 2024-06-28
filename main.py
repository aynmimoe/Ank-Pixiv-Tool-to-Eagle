import txtDict_to_eagleDict
import jsonDict_to_eagleDict
import eagle_folder
import os
import requests

eagle_api_url = 'http://localhost:41595'

if __name__ == "__main__":
    import sys

    # 取得帶入的參數
    try:
        basePath = sys.argv[1]
    except IndexError as e:
        basePath = "./sample/"

    # 取得Eagle所有資料夾名單
    eagle_all_folders = eagle_folder.getEagleAllFolder()
    fileCount = 0
    errorFilePath = []
    # 掃描所有檔案
    for root, dirs, files in os.walk(basePath, topdown=False):
        for fileName in files:
            fileCount = fileCount+1
            fileNameWithoutExt = fileName.split('.')[0]
            fileExt = fileName.split('.')[-1]
            baseFilePath = os.path.join(root)
            filePath = os.path.join(baseFilePath, fileName)
            print(str(fileCount)+": "+filePath)

            # 若該檔案名稱是meta，代表這個資料夾是一個圖集
            # maxNum = 0
            filePathList = []
            if fileNameWithoutExt == 'meta':
                folderFileList = os.listdir(baseFilePath)
                folderFileList.sort()
                for theFile in folderFileList:
                    thePath = os.path.join(baseFilePath, theFile)
                    theExt = theFile.split('.')[-1]
                    # print(theFile)
                    if theExt in ['txt','json']:
                        continue
                    else:
                        filePathList.append(thePath)
                # print(filePathList)
                
                # # 計算圖片數量
                # folderFileList = os.listdir(baseFilePath)
                # nameList = list(map(lambda x: x.split('.')[0] ,folderFileList))
                # nameList.sort(reverse=True)
                # for theName in nameList:
                #     try:
                #         int(theName)
                #         maxNum = int(theName)
                #         break
                #     except ValueError:
                #         continue
                #     else:
                #         continue

            # 製作Eagle Request Body
            if fileExt == 'txt':
                txtDict = txtDict_to_eagleDict.readFile_to_txtDict(filePath)
                if txtDict == {}:
                    errorFilePath.append(filePath)
                    continue
                eagleData = txtDict_to_eagleDict.txtDict_to_eagleDict(txtDict, filePath, filePathList)
                pUserId = txtDict_to_eagleDict.txtDict_to_puserId(txtDict)
                pUserName = txtDict_to_eagleDict.txtDict_to_puserName(txtDict)
            elif fileExt == 'json':
                jsonDict = jsonDict_to_eagleDict.readFile_to_jsonDict(filePath)
                if jsonDict == {}:
                    errorFilePath.append(filePath)
                    continue
                eagleData = jsonDict_to_eagleDict.jsonDict_to_eagleDict(jsonDict, filePath, filePathList)
                pUserId = jsonDict_to_eagleDict.jsonDict_to_puserId(jsonDict)
                pUserName = jsonDict_to_eagleDict.jsonDict_to_puserName(jsonDict)
            else:
                continue

            # 查詢Eagle資料夾id
            eagleFolder = eagle_folder.search_folder(eagle_all_folders, pUserName, pUserId)
            if eagleFolder is not None:
                eagleFolderId = eagleFolder.get('id')
            else:
                authorName = pUserName
                pid = pUserId
                eagleFolderId = eagle_folder.createFolder(authorName, pid)
                eagle_all_folders = eagle_folder.getEagleAllFolder() # 再重新更新一次清單

            folderData = {
                "folderId": eagleFolderId
            }

            data = eagleData | folderData
            # print(data)

            # 新增檔案到Eagle
            if data is not None:
                isMultiItem = data.get('items') is not None

                if isMultiItem:
                    addResp = requests.post(eagle_api_url+'/api/item/addFromPaths', json=data)
                else:
                    addResp = requests.post(eagle_api_url+'/api/item/addFromPath', json=data)
                    
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
    
    print('Error Files: ==================================')        
    print(errorFilePath)