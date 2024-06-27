# https://chatgpt.com/c/1eb95fd6-d3da-4502-aede-fe03239784f9
#
# 注意事項：

#    正則表達式：Python使用re模組進行正則表達式匹配，這與JavaScript中的正則表達式類似，但具體的匹配方法和語法稍有不同。
#    字典和屬性訪問：在Python中，使用.get()方法來獲取字典中的值，這可以避免因為鍵不存在而引發錯誤。
#    字符串操作：Python中的字符串操作方法與JavaScript略有不同，例如使用.split()方法拆分字符串，使用+=來拼接字符串。
#    遞歸調用：在Python中同樣可以遞歸調用函數，這與JavaScript的方式基本相同。
#
#這樣的轉換讓Python函數能夠實現與原始JavaScript函數相同的功能。如果有任何疑問或需要進一步的說明，請隨時告訴我！

def search_folder(folders, author, pid):
    for folder in folders:
        description = folder.get('description', '')
        if description:
            match = re.search(r'(?<=pid ?[:=] ?)\d+', description)
            if match and match.group(0) == pid:
                return folder
            elif folder.get('name') == author:
                return folder
            elif match and match.group(0) != pid:
                continue
            else:
                new_description = ""
                for line in description.split("\n"):
                    if not re.match(r'^ *pid ?[:=] ?', line):
                        new_description += "\n" + line
                update_folder({
                    "folderId": folder.get('id'),
                    "newDescription": f"pid = {pid}{new_description}"
                })
                return folder
        else:
            for child_folder in folder.get('children', []):
                target = search_folder(child_folder, author, pid)
                if target:
                    return target
