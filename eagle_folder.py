import requests
import json
import regex

eagle_all_folders = []

eagle_api_url = 'http://localhost:41595'

def getEagleAllFolder():
    response = requests.get(eagle_api_url+'/api/folder/list')
    global eagle_all_folders
    eagle_all_folders = response.json()['data']
    return eagle_all_folders

def search_folder(folders, author, pid):
    # print(folders[3]['description'])
    # return None
    for folder in folders:
        description = folder.get('description', None)
        match = None
        if description is not None:
            match = regex.search(r'(?<=pid ?[:=] ?)\d+', description)
        # 如果描述中的pid吻合 OR 作者名字吻合
        if (match is not None and match.group(0) == pid) or folder.get('name') == author:
            if match.group(0) is not None and match.group(0) != pid:
                continue
            # 如果該資料夾有pid，但不吻合，就確定不是這個
            else:
                # new_description = ""
                # for line in description.split("\n"):
                #     if not re.match(r'^ *pid ?[:=] ?', line):
                #         new_description += "\n" + line
                # update_folder({
                #     "folderId": folder.get('id'),
                #     "newDescription": f"pid = {pid}{new_description}"
                # })
                pass
            return folder

    for folder in folders:
        child_folders = folder.get('children', [])
        target = search_folder(child_folders, author, pid)
        if target is not None:
            return target

if __name__ == "__main__":
    import sys

    getEagleAllFolder()
    # print(eagle_all_folders)

    thisFolder = search_folder(eagle_all_folders, None, '264932')
    print(thisFolder)