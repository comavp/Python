def list_to_string(list):
    res = ''
    listSize = len(list)
    for ind in range(listSize):
        if ind > 0 and ind < listSize - 1:
            res += ', '
        elif ind == listSize - 1 and listSize != 1:
            res += ' and '
        res += str(list[ind])
    return res

print(list_to_string([1, 2, 3, 4]))
print(list_to_string([1, 2]))
print(list_to_string(['test1', 2, 'test3']))
