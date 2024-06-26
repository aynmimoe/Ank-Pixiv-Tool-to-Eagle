
def group_hierarchy_split2(test_dict, splt_chr):
    result = {}
    for key in test_dict:
        key_parts = key.split(splt_chr)
        inner_dict = add_to_dict(key_parts[1:], test_dict[key])
        result.setdefault(key_parts[0], {}).update(inner_dict)
    return result

def add_to_dict(keys, value):
    if not keys:
        return value
    key = keys.pop(0)
    return {key: add_to_dict(keys, value)}

test_dict = {"1-3" : 2, "8-3-7" : 99888, "1-8" : 10, "8-6" : 15, "8-3-6" : 15}
splt_chr = "-"
print(group_hierarchy_split2(test_dict, splt_chr))

